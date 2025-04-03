from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, AvailableSlot
from .serializers import UserProfileSerializer, AvailableSlotSerializer

class UpdateUserDetails(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id = None):
        if user_id:
            try:
                user = UserProfile.objects.get(id=user_id)
                serializer = UserProfileSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id = None):
        if user_id:
            try:
                user = UserProfile.objects.get(id=user_id)
                serializer = UserProfileSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except UserProfile.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id=None):
        if user_id:
            try:
                user = UserProfile.objects.get(id=user_id)
                user.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

# View for slot creation (POST)
class CreateAvailableSlots(APIView):
    def post(self, request, user_id):
        try:
            # Ensure the user exists
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get slots data from the request
        slots_data = request.data.get("slots", [])
        if not isinstance(slots_data, list):
            return Response({"error": "Slots data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        # Iterate through each slot and validate using the serializer
        errors = []
        created_slots = []
        for slot in slots_data:
            slot["user"] = user.id  # Assign the user to each slot
            serializer = AvailableSlotSerializer(data=slot)
            if serializer.is_valid():
                saved_slot = serializer.save()
                created_slots.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Slots created successfully!", "slots": created_slots},
            status=status.HTTP_201_CREATED
        )

# View for slot update (PUT)
class UpdateAvailableSlot(APIView):
    def put(self, request, slot_id):
        try:
            # Fetch the specific slot by its ID
            slot = AvailableSlot.objects.get(id=slot_id)
        except AvailableSlot.DoesNotExist:
            return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate and update the slot with new data
        serializer = AvailableSlotSerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            updated_slot = serializer.save()
            return Response(
                {"message": "Slot updated successfully!", "slot": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
