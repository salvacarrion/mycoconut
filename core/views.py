from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def demo(request):
    return render(request, 'core/demo.html')
