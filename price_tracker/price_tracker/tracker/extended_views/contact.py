from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from ..forms import ContactForm
from ..models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            user_message = f"User {form.cleaned_data['name']} with email address: {form.cleaned_data['email']} said: \n{form.cleaned_data['message']}"
            # Send email (optional)
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['subject']}",
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            form = ContactForm()  # Reset the form
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
