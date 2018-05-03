from rest_framework import serializers
from .models import Timeline, Note

class TimelineSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='rest_replica:micro-timeline-note-list', lookup_field='slug')

    class Meta:
        model = Timeline
        fields = ('id', 'user', 'date_created', 'date_updated', 'name', 'slug', 'rev_order', 'is_public', 'id', 'api_url')

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    #timeline = TimelineSerializer(many=False, required=False)
    api_url = serializers.HyperlinkedIdentityField( view_name='rest_replica:micro-note-detail', lookup_field='id')

    class Meta:
        model = Note
        fields = ('id', 'user', 'date_created', 'date_updated', 'is_private', 'body_html', 'api_url')

class NoteCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timeline = TimelineSerializer(many=False, required=False)
    api_url = serializers.HyperlinkedIdentityField( view_name='rest_replica:micro-note-detail', lookup_field='id')

    class Meta:
        model = Note
        fields = ('id', 'user', 'date_created', 'date_updated', 'timeline', 'is_private', 'body', 'api_url')
