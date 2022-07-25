from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import auth, User
from django.contrib import messages


class LoginView(View):

    def get(self, request):
        return render(request,'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('/accounts/login')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')


class RegisterView(View):

    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/accounts/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/accounts/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('/accounts/login')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('/accounts/register')


class AccountView(View):

    def get(self, request):
        render(request, 'accounts/detail.html')
