from django.urls import path

from bipolar.views.index import index
from bipolar.views.github import gh_listener
from bipolar.views.logger import log

urlpatterns = [
    path('', index, name='index'),
    path('gh', gh_listener, name='gh_listener'),
    path('log', log, name="log")
]
