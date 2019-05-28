from django.http import HttpResponse
from django.shortcuts import render


def home_view(request, *args, **kwargs):
  # print(args, kwargs)
  # print(request.user)
  return render(request, 'home.html', {})


def contact_view(request, *args, **kwargs):
  context = {
    'my_text': 'This is about us',
    'this_is_true': True,
    'my_number': 123,
    'my_list': [312, '3543', 'sdfsdf', 567]
  }
  return render(request, 'contact.html', context) 
