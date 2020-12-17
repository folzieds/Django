from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, HttpResponseRedirect
from .models import Tutorial,EmailSender
from django.contrib.auth.forms import UserCreationForm
from .EmailService import EmailService
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name='main/home.html',
                  context={'tutorials': Tutorial.objects.all(),
                           'count':Tutorial.objects.all().count()})

def search(request):
    if request.method == "GET":
        form = request.GET.get('q')

        return render(request,
                      'main/home.html',
                      {'tutorials': Tutorial.objects.filter(tutorial_content__contains=f'{form}'),
                       'count':Tutorial.objects.filter(tutorial_content__contains=f'{form}').count()}
                      )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"New User {username} created")
            login(request, user)

            return HttpResponseRedirect("main:main_homepage")
        else:
            for msg in form.error_messages:
                #log the error here
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = UserCreationForm
    return render(request,
                  'main/register.html',
                  {'form':form}
                  )

def email(request):
    if request.method == "GET":
        form = EmailSender()
        form.email_body = request.GET.get("message")
        form.contact_name = request.GET.get("contact")
        form.contact_email = request.GET.get("email")
        if form.is_valid():
            email_request = EmailService(form)

            email_request.send_email_ssl()

    return HttpResponseRedirect(request.META['SERVER_NAME'])

