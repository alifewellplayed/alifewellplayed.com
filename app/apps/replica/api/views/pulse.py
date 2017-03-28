import hashlib

from rest_framework import generics, permissions, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import *
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from django.conf import settings

from coreExtend.models import Account as User
from replica.pulse.models import Entry, Draft, Media, Topic, Channel, MenuPosition, MenuItem, EntryLink, SiteSettings
from replica.contrib.micro.models import Timeline, Note
from replica.api.serializers import *
from replica.api.permissions import IsOwner, IsOwnerOrReadOnly
from replica import settings as r_settings


class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Topic.objects.public()
    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class TopicList(generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            topics = Topic.objects.filter(
                Q(is_public=True) |
                Q(user__username=request_user.username)
            )
            return topics
        else:
            return Topic.objects.filter(is_public=True)

class TopicEntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries.filter(topic__slug=self.kwargs.get('slug'))
        else:
            return Entry.objects.published().filter(topic__slug=self.kwargs.get('slug'))

class EntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.posts().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries
        else:
            return Entry.objects.published()

class ChannelList(generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = ChannelSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Channel.objects.all()

class ChannelEntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries.filter(channel__slug=self.kwargs.get('slug'))
        else:
            return Entry.objects.published().filter(channel__slug=self.kwargs.get('slug'))

class EntryDraftList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        request_user = self.request.user
        entries = Entry.objects.ideas().filter(user__username=request_user.username)
        return entries

class EntryUpcomingList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        request_user = self.request.user
        entries = Entry.objects.upcoming().filter(user__username=request_user.username)
        return entries

class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        """Force user to the current user on save"""
        obj.user = self.request.user
        return super(EntryDetail, self).pre_save(obj)

class EntryCreate(generics.CreateAPIView):
    lookup_field = 'id'
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        return super(EntryCreate, self).perform_create(serializer)

class PageList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.pages().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries
        else:
            return Entry.objects.pages_published()

class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Entry.objects.pages_published()
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        """Force user to the current user on save"""
        obj.user = self.request.user
        return super(PagesDetail, self).pre_save(obj)


class CurrentSite(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):

        u = get_object_or_404(User, username=request.user.username)
        a = hashlib.md5(u.email.encode('utf-8')).hexdigest()
        avatar = "https://secure.gravatar.com/avatar/%s.jpg" % a

        user_settings = {
            "current_user": u.username,
            "current_user_hash": a,
            "current_avatar": avatar,
            'AccountSettings': reverse('CoreExtend:AccountSettings'),
            'password_change': reverse('CoreExtend:password_change'),
            'logout': reverse('CoreExtend:Logout'),
        }
        site_settings = {
            "site_name": r_settings.SITE_NAME,
            "site_url": r_settings.SITE_URL,
        }
        settings = {
            'site_settings': site_settings,
            'user_settings': user_settings,
        }

        return Response(settings)

class CurrentSiteStats(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):

        request_user = request.user

        topics = Topic.objects.all()
        channels = Channel.objects.all()
        published_e = Entry.objects.published()
        upcoming_e = Entry.objects.upcoming()
        ideas_e = Entry.objects.ideas()
        pages_e = Entry.objects.pages()
        media = Media.objects.all()
        notes = Note.objects.all()

        total_counts = {
            'topics': topics.count(),
            'channels': channels.count(),
            'published': published_e.count(),
            'upcoming': upcoming_e.count(),
            'ideas': ideas_e.count(),
            'pages': pages_e.count(),
            'media': media.count(),
            'notes': notes.count()
        }
        user_counts = {
            'published': published_e.filter(user=request_user).count(),
            'upcoming': upcoming_e.filter(user=request_user).count(),
            'ideas': ideas_e.filter(user=request_user).count(),
            'pages': pages_e.filter(user=request_user).count(),
            'media': media.filter(user=request_user).count(),
            'notes': notes.filter(user=request_user).count()
        }
        counts = {
            'total_counts': total_counts,
            'user_counts': user_counts
        }
        return Response(counts)

class CurrentSiteSettings(generics.RetrieveUpdateAPIView):
    model = SiteSettings
    lookup_field = 'id'
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SiteSettingsSerializer

    def get(self, request, format=None):
        site_id = SiteSettings.objects.get(id=settings.SITE_ID)
        serializer = SiteSettingsSerializer(site_id)
        return Response(serializer.data)

    def put(self, request, format=None):
        site_id = SiteSettings.objects.get(id=settings.SITE_ID)
        serializer = SiteSettingsSerializer(site_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

class DashboardView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        count_total = 10
        request_user = request.user

        def DataObj(ObjQuery=None, ObjSerializer=None):
            o = ObjQuery
            object_obj = ObjSerializer(o[:count_total], many=True, context={'request': request})
            object_data = {
                'count': {'mine': o.filter(user=request_user).count(), 'total': o.count()},
                'results': object_obj.data
            }
            return object_data

        data = {
            'topics': DataObj(Topic.objects.all(), TopicSerializer),
            'channels': DataObj(Channel.objects.all(), ChannelSerializer),
            'media': DataObj(Media.objects.all(), MediaSerializer),
            'published_entries': DataObj(Entry.objects.published(), EntrySerializer),
            'upcoming_entries': DataObj(Entry.objects.upcoming(), EntrySerializer),
            'ideas': DataObj(Entry.objects.ideas(), EntrySerializer),
            'pages': DataObj(Entry.objects.pages(), EntrySerializer),
        }
        return Response(data)
