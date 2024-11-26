from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


def login_view(request):

     # Redirect to home if the user is already logged in
    if request.user.is_authenticated:
        return redirect('home')  # Replace 'home' with your desired view name

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in and redirect
            print(username, password)
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect
        else:
            # If authentication fails, show an error message
            print(password, username)
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
