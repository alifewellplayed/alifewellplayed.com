from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from coreExtend.models import Account as User
from replica.api.permissions import IsOwner, IsOwnerOrReadOnly
from replica import settings as r_settings

from .models import Timeline, Note
from .serializers import *


#Lists all notes request.user has access to
class NoteList(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            notes = Note.objects.filter(
                Q(is_private=False) |
                Q(user__username=request_user.username)
            )
            return notes
        else:
            return Note.objects.filter(is_private=False)

class TimelineList(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            timelines = Timeline.objects.filter(
                Q(is_public=True) |
                Q(user__username=request_user.username)
            )
            return timelines
        else:
            return Timeline.objects.filter(is_public=True)

class UserTimelineList(generics.ListAPIView):
    lookup_field = 'username'
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        request_user = self.request.user
        user = self.kwargs['username']
        if request_user.username == user:
            return Timeline.objects.filter(user__username=user)
        else:
            return Timeline.objects.filter(user__username=user).filter(is_public=True)

class UserNoteList(generics.ListAPIView):
    lookup_field = 'username'
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        request_user = self.request.user
        user = self.kwargs['username']
        if request_user.username == user:
            return Note.objects.filter(user__username=user)
        else:
            return Note.objects.filter(user__username=user).filter(is_private=False)

class TimelineNoteList(generics.ListAPIView):
    model = Note
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            notes = Note.objects.filter(
                Q(is_private=False) |
                Q(user__username=request_user.username)
            )
            return notes.filter(timeline__slug=self.kwargs.get('slug'))
        else:
            return Note.objects.filter(is_private=False).filter(timeline__slug=self.kwargs.get('slug'))

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class NoteCreate(generics.CreateAPIView):
    lookup_field = 'id'
    model = Note
    serializer_class = NoteSerializer
    permission_classes = [ IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TimelineCreate(generics.CreateAPIView):
    lookup_field = 'slug'
    model = Timeline
    serializer_class = TimelineSerializer
    permission_classes = [ IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
