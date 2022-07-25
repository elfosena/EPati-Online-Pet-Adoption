from django.shortcuts import render
from django.views.generic import View

from adopt.models import Kind

# Create your views here.


class BaseView(View):
    context = {}

    def __init__(self):
        self.context = {
            'kind_set': Kind.objects.all(),
        }
