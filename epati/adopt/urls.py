from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

app_name = 'adopt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('adopt/<int:pk>/', views.PetDetailView.as_view(), name='detail'),
    path('addpet', views.AddPet.as_view(), name='addpet'),
    path('adopt/<int:pk>/update_pet', views.UpdatePetView.as_view(), name='update_pet'),
    path('adopt/<int:pk>/delete_pet', views.DeletePetView.as_view(), name='delete_pet'),
    path('adopt/pets', views.AllPetsListView.as_view(), name='pets'),
    path('adopt/pets/<str:kind>', views.PetListView.as_view(), name='pets_kind'),
    path('adopt/my_pets', views.MyPetsListView.as_view(), name='my_pets'),
    path('adopt/my_listings', views.MyListingsListView.as_view(), name='my_listings'),
    path('adopt/favorites', views.FavoritePetsListView.as_view(), name='favorite_pets'),
    path('search', csrf_exempt(views.SearchView.as_view()), name="search"),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('favorite', views.FavoriteAddView.as_view(), name='favorite_add'),
    path('adopt/request', views.AdoptRequestView.as_view(), name='adopt_request'),
    path('adopt/request_list', views.AdoptRequestsListView.as_view(), name="request_list"),
    path('adopt/request_action', views.AdoptRequestActionView.as_view(), name="request_action"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)