from django.urls import path

from bipolar.views.index import index
from bipolar.views.github import gh_listener
from bipolar.views.logger import login, logout

urlpatterns = [
    path('', index, name='index'),
    path('gh', gh_listener, name='gh_listener'),
    path('log/login', login, name="log_login"),
    path('log/logout', logout, name="log_logout")
]
