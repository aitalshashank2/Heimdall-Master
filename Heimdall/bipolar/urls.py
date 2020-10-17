from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gh', views.gh_listener, name='gh_listener')
]
