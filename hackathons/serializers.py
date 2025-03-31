from rest_framework import serializers
from .models import HackathonsList, HackathonApplication
from accounts.models import CustomUser  # Import CustomUser model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']  # Add relevant user fields

class HackathonSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Nest user details
    class Meta:
        model = HackathonsList
        fields = ['id', 'title', 'description', 'prize', 'start_date', 'end_date', 'status', 'created_by']

class HackathonApplicationSerializer(serializers.ModelSerializer):
    hackathon_title = serializers.CharField(source="hackathon.title", read_only=True)  #  Include Hackathon Title
    user_email = serializers.EmailField(source='user.email', read_only=True) # Auto fetch user email
    
    class Meta:
        model = HackathonApplication
        fields = ['id', 'hackathon', 'hackathon_title', 'user_email', 'applied_at']  #  Include all required fields
        extra_kwargs = {'hackathon': {'required': False}}  # ✅ Make hackathon field optional

    def create(self, validated_data):
        hackathon = self.context['hackathon']  # Get hackathon from context
        return HackathonApplication.objects.create(hackathon=hackathon, **validated_data)

        