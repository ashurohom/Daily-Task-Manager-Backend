# posts/serializers.py - CORRECTED VERSION
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'due_date': {'required': False, 'allow_null': True},
            'title': {'required': True},
            'priority': {'required': False, 'default': 'medium'},
            'status': {'required': False, 'default': 'pending'},
        }