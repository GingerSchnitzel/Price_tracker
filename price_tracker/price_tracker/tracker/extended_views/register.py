from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from ..forms import UserRegistrationForm

def register(request):  
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect
    else:
        form = UserRegistrationForm()
    base_template = "base.html" if request.user.is_authenticated else "login_base.html"
    return render(request, 'register.html', {'form': form, 'already_logged_in' : request.user.is_authenticated, 'base_template' : base_template })