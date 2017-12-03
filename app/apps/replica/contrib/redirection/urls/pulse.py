from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from replica.contrib.redirection.views import pulse as views

app_name="replica.redirection"
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', views.LinkRedirect, name = 'link_redirect'),
]
