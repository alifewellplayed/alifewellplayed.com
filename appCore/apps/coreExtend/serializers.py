from rest_framework import serializers

from .models import Account

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'gender', 'location', 'url')
