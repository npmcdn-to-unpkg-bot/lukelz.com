from django.contrib.auth.models import User
from rest_framework import serializers

from .models import NonMediaItem

class UserSerializer(serializers.ModelSerializer):
    nonmediaitems = serializers.PrimaryKeyRelatedField(many=True, queryset=NonMediaItem.objects.all())

    class Meta:
            model = User
            fields = ('id', 'username', 'nonmediaitems')

class NonMediaItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = NonMediaItem
        fields = '__all__'