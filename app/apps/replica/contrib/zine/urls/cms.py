from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from replica.contrib.zine import views

app_name="replica.zine"
urlpatterns = [
    url(r'^$', login_required(views.Index), name="ZineIndex"),
    url(r'^promoted/$', login_required(views.PromotedEdit), name="PromotedNew"),
    url(r'^promoted/edit/(?P<promotedID>[\w-]+)/$', login_required(views.PromotedEdit), name = "PromotedEdit"),
    url(r'^promoted/edit/(?P<promotedID>[\w-]+)/delete/$', login_required(views.PromotedDelete), name = "PromotedDelete"),
    #url(r'^collections/$', login_required(views.Index), name="CollectionsList"),
    #url(r'^collections/edit/(?P<collectionID>[\w-]+)/$', login_required(views.CollectionEdit), name = "CollectionEdit"),
    #url(r'^collections/edit/(?P<collectionID>[\w-]+)/delete/$', login_required(views.CollectionDelete), name = "CollectionDelete"),
]
