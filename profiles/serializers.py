from rest_framework import serializers
from .models import UserProfile, AvailableSlot

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'    # name, email, phone number

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = '__all__'     # user, date, time, available
