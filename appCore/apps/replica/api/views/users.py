from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import generics, permissions, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from replica.api.serializers import *
from replica.api.permissions import *
from coreExtend.models import Account as User

class UserList(generics.ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    paginate_by = 100

class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

class CurrentUser(APIView):
    lookup_field = 'username'
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
