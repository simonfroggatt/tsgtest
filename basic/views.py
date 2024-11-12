from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the tsgtest/basic index.")

def temp_test(request):
    template = "basic/tmp_test.html"
    data = {'title': 'This is a test'}
    return render(request, template, data)
