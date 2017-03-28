from rest_framework import serializers
from django.conf import settings
from replica.pulse.models import Entry, Draft, Media, Topic, Channel, MenuPosition, MenuItem, EntryLink, SiteSettings
from coreExtend.models import Account as User

class MediaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Media
        fields = ('id', 'user', 'title', 'caption', 'content', 'image', 'thumbnail_small', 'thumbnail_medium', 'url')

class ChannelSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='rest_replica:channel-detail', lookup_field='slug')

    class Meta:
        model = Channel
        fields = ('id', 'user', 'title', 'slug', 'api_url')

class TopicSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='rest_replica:topic-detail', lookup_field='slug')
    image = MediaSerializer()

    class Meta:
        model = Topic
        fields = ('id', 'user', 'title', 'slug', 'description', 'image', 'api_url' )

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    topic = TopicSerializer(many=True, required=False, allow_null=True)
    channel = ChannelSerializer(many=False, required=False, allow_null=True)
    image = MediaSerializer(many=False, read_only=True)
    api_url = serializers.HyperlinkedIdentityField(view_name='rest_replica:entry-detail', lookup_field='id')

    class Meta:
        model = Entry
        fields = ('title', 'slug', 'url', 'user', 'topic', 'pub_date', 'is_active', 'channel', 'total_words',
        'content_format', 'deck', 'deck_html', 'body', 'body_html', 'image', 'id', 'api_url', 'date_updated', 'date_created')

class DraftSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Draft
        fields = ('id', 'title', 'slug', 'content_format', 'deck', 'deck_html', 'body', 'body_html', 'user', 'date_created', 'date_updated')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'hash', 'gender', 'location', 'url')

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('id', 'domain', 'name', 'is_enabled', 'password', 'view_settings', 'secret_token', 'view_settings', 'author', 'date_created', 'date_updated')
