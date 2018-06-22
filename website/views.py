from django.shortcuts import redirect, render, HttpResponse
from django.template import loader


def home_redirect(request):
    return redirect('/dataProfile/')
# Want to change this so it goes to the accounts app
# Create your views here.
# def home(request):
#     return HttpResponse(loader.get_template('farm.html').render())
