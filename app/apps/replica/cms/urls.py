from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    url(r'^$',login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/base.html"))), name="App" ),
    url(r'^(?P<path>.*)/$', login_required(ensure_csrf_cookie(TemplateView.as_view(template_name="replica/cms/base.html"))), name="App" ),
]
