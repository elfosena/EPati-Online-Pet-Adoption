from queue import Empty
from django.views.generic import View
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse

from chat.models import Thread
from adopt.models import Pet, Kind, AdoptionRequest
from adopt.forms import PetCreateForm
from adopt.models import ADOPTION_REQUEST_STATUS
from common.utils import pagination_helper
from common.views import BaseView

class IndexView(BaseView):
    
    def get(self, request):

        self.context.update({
            'dog_list': Pet.recent_dog_list(),
            'cat_list': Pet.recent_cat_list(),
            'other_list' : Pet.recent_other_list(),
        })
        return render(request, 'adopt/index.html', self.context)


class FavoriteAddView(LoginRequiredMixin, View):

    def post(self, request):
        pk = int(request.POST.get('pet_id'))
        pet = get_object_or_404(Pet, pk=pk)
        if pet.favorites.filter(id=request.user.id).exists():
            pet.favorites.remove(request.user)
            favorite = False
        else:
            pet.favorites.add(request.user)
            favorite = True
        pet.save()
        return JsonResponse({'favorite': favorite})


class AdoptRequestActionView(LoginRequiredMixin, BaseView):

    def post(self, request):
        adoption_request = get_object_or_404(AdoptionRequest, id=request.POST.get('adoption_request'))
        accepted = request.POST.get('accepted')
        pet = adoption_request.pet
        requests_to_reject = list(AdoptionRequest.objects.filter(pet=pet))
        print(requests_to_reject)

        if accepted == 'true':
            pet.adopted = True
            pet.adopted_by = adoption_request.sender
            pet.save()
            for request in requests_to_reject:
                request.status = ADOPTION_REQUEST_STATUS[3][0]
                request.save()
            adoption_request.status = ADOPTION_REQUEST_STATUS[1][0]
        else:
            adoption_request.status = ADOPTION_REQUEST_STATUS[2][0]

        adoption_request.save()
        return JsonResponse({'accepted': accepted})


class AdoptRequestsListView(LoginRequiredMixin, BaseView):

    def get(self, request):
        requests_recieved = AdoptionRequest.objects.filter(reciever=request.user)
        requests_sent = AdoptionRequest.objects.filter(sender=request.user)

        self.context.update({
            'requests_recieved': requests_recieved,
            'requests_sent': requests_sent,
        })
        return render(request, 'adopt/requests.html', self.context)


class AdoptRequestView(LoginRequiredMixin, View):

    def post(self, request):
        pk = int(request.POST.get('pet_id'))
        pet = get_object_or_404(Pet, pk=pk)

        adoption_request = AdoptionRequest.objects.filter(Q(reciever=pet.published_by) & Q(sender=request.user) & Q(pet=pet))

        if adoption_request.exists():
            adoption_request.delete()
            request_sent = False
        else:
            adoption_request = AdoptionRequest.objects.create(reciever=pet.published_by, sender=request.user, pet=pet)
            adoption_request.save()
            request_sent = True

        return JsonResponse({'request_sent': request_sent})


class SearchView(BaseView):

    def post(self, request):
        search_str = request.POST.get('search_str')
        search_type = request.POST.get('search_type')

        if len(search_str) == 0:
            self.context.update({
                'dog_list': Pet.recent_dog_list(),
                'cat_list': Pet.recent_cat_list(),
                'other_list' : Pet.recent_other_list(),
            })
            return render(request, 'adopt/recently_added.html', self.context)

        else:
            search_results = Pet.get_listings().filter(Q(name__icontains=search_str) |        
                Q(description__icontains=search_str) | 
                Q(kind__name__icontains=search_str) |
                Q(breed__icontains=search_str) | 
                Q(age__icontains=search_str) | 
                Q(description__icontains=search_str))

            pet_list = list(search_results.values())
            self.context.update({
                'kind': 'Search Result',
                'pet_list': pet_list,
            })
            return render(request, 'adopt/search_results.html', self.context)


class ContactView(BaseView):

    def get(self, request):
        return render(request, 'adopt/contact.html', self.context)


class PetDetailView(BaseView): 

    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)

        if pet.is_active:
            favorite = pet.favorites.filter(id=request.user.id).exists()
            request_sent = AdoptionRequest.objects.filter(Q(reciever=pet.published_by) & Q(sender=request.user) & Q(pet=pet)).exists()
            self.context.update({
                'pk': pk,
                'pet': pet,
                'favorite': favorite,
                'request_sent': request_sent,
            })
            return render(request, 'adopt/detail.html', self.context)
        else:
            return redirect('/')


class PetListView(BaseView):

    def get(self, request, kind):
        pet_list = pagination_helper(Pet.get_listings().filter(kind=get_object_or_404(Kind, name=kind)), request.GET.get('page', 1), 12)
        self.context.update({
            'pet_list': pet_list,
            'kind': kind,
        })
        return render(request, 'adopt/pets.html', self.context)


class AddPet(LoginRequiredMixin, BaseView):

    def get(self, request):
        form = PetCreateForm()
        self.context.update({
            'form': form,
        })

        return render(request, 'adopt/pet_form.html', self.context)
        
    def post(self, request):
        form = PetCreateForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.published_by = request.user
            kind_str = request.POST['pet_kind'].lower().capitalize().strip()
            if Kind.objects.filter(name=kind_str).exists():
                kind = Kind.objects.get(name=kind_str)
            else:
                kind = Kind(name=kind_str)
                kind.save()
            instance.kind = kind
            instance.name = instance.name.lower().capitalize()
            instance.save()

            pet = get_object_or_404(Pet, pk=instance.id)
            favorite = False
            if pet.favorites.filter(id=request.user.id).exists():
                favorite = True
            self.context.update({
                'pk': instance.id,
                'pet': pet,
                'favorite': favorite,
            })
            return render(request, 'adopt/detail.html', self.context)

        self.context.update({'form': form})

        return render(request, 'adopt/pet_form.html', self.context)


class UpdatePetView(LoginRequiredMixin, BaseView):

    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        if pet.published_by != request.user:
            return redirect('/')
        elif pet.is_active == False:
            return redirect('/')
        else:
            form = PetCreateForm(instance=pet)
            self.context.update({
                'form': form,
                'pet': pet,
            })
            return render(request, 'adopt/pet_form.html', self.context)

    def post(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        form = PetCreateForm(request.POST, request.FILES, instance=pet)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.published_by = request.user
            kind_str = request.POST['pet_kind'].lower().capitalize().strip()
            if Kind.objects.filter(name=kind_str).exists():
                kind = Kind.objects.get(name=kind_str)
            else:
                kind = Kind(name=kind_str)
                kind.save()
            instance.kind = kind
            instance.name = instance.name.lower().capitalize()
            instance.save()

            pet = get_object_or_404(Pet, pk=instance.id)
            favorite = False
            if pet.favorites.filter(id=request.user.id).exists():
                favorite = True

            self.context.update({
                'pk': instance.id,
                'pet': pet,
                'favorite': favorite,
            })
            return render(request, 'adopt/detail.html', self.context)

        self.context.update({'form': form})

        return render(request, 'adopt/pet_form.html', self.context)


class DeletePetView(LoginRequiredMixin, BaseView):

    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        if pet.published_by != request.user:
            return redirect('/')
        elif pet.is_active == False:
            return redirect('/')
        else:
            self.context.update({
                'pet': pet,
            })
            return render(request, 'adopt/delete_pet.html', self.context)

    def post(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        pet.delete()
        self.context.update({
            'pet_list': pagination_helper(Pet.get_listings().filter(published_by=request.user), request.GET.get('page', 1), 12),
            'kind': "My Pet",
        })
        return render(request, 'adopt/pets.html', self.context)


class MyPetsListView(LoginRequiredMixin, BaseView):

    def get(self, request):
        pet_list = pagination_helper(Pet.objects.filter(adopted_by=request.user), request.GET.get('page', 1), 12)

        self.context.update({
            'pet_list': pet_list,
            'kind': "My Pet",
        })
        return render(request, 'adopt/pets.html', self.context)


class MyListingsListView(LoginRequiredMixin, BaseView):

    def get(self, request):
        pet_list = pagination_helper(Pet.get_active().filter(published_by=request.user), request.GET.get('page', 1), 12)

        self.context.update({
            'pet_list': pet_list,
            'kind': "My Listing",
        })
        return render(request, 'adopt/pets.html', self.context)


class FavoritePetsListView(LoginRequiredMixin, BaseView):

    def get(self, request):
        pet_list = pagination_helper(request.user.favorite.filter(is_active=True), request.GET.get('page', 1), 1)

        self.context.update({
            'pet_list': pet_list,
            'kind': "Favorite Pet",
        })
        return render(request, 'adopt/pets.html', self.context)


class AllPetsListView(BaseView):

    def get(self, request):
        pet_list = pagination_helper(Pet.get_listings().all(), request.GET.get('page', 1), 12)

        self.context.update({
            'pet_list': pet_list,
            'kind': "All Pet",
        })
        return render(request, 'adopt/pets.html', self.context)