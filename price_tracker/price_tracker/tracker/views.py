from django.shortcuts import redirect

def main_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return redirect ('login')