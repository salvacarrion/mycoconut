"""mycoconut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core.views import views, views_ajax

urlpatterns = [
    path('', views.index, name='index'),
    path('demo/', views.demo, name='demo'),
    path('dolly/', views.dolly, name='dolly'),
    path('dolly/<str:job_id>/', views.dolly_get_job, name='dolly_get_job'),  # Used to returned a cache result
    path('ajax/get-number/', views_ajax.get_number, name='get_number'),
    path('ajax/check-job-status/', views_ajax.check_job_status, name='check_job_status'),
]
