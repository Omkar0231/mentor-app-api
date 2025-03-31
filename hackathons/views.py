from django.shortcuts import get_object_or_404
from .models import HackathonsList
from rest_framework.views import APIView
from .serializers import HackathonSerializer, HackathonApplicationSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from .models import HackathonsList, HackathonApplication
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.auth import TokenAuthentication
from accounts.models import CustomUser  # Import your user model


# Create your views here.

class HackathonsListView(APIView):
    authentication_classes = [TokenAuthentication]  # ✅ Use Knox Authentication
    permission_classes = [AllowAny]  # ✅ Ensure user is logged in
    
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # ✅ Require authentication for POST
        self.authentication_classes = [TokenAuthentication]  # ✅ Knox authentication
        self.check_permissions(request)

        user = request.user  # ✅ Get the logged-in user from Knox token
        serializer = HackathonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=user)  # ✅ Automatically set 'created_by'
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        status_filter = request.query_params.get('status')

        if status_filter is not None:
            query_set = HackathonsList.objects.filter(status=status_filter.lower() == 'true')
        else:
            query_set = HackathonsList.objects.all()

        serializer = HackathonSerializer(query_set, many=True)
        return Response({'data': serializer.data})
    
# ✅ Retrieve, Update, and Delete Hackathon by ID
class HackathonView(APIView):
    authentication_classes = [TokenAuthentication]  # ✅ Use Knox Authentication
    permission_classes = [AllowAny]  # ✅ Ensure user is logged in

    def get(self, request, pk, *args, **kwargs):
        hackathon = get_object_or_404(HackathonsList, id=pk)
        serializer = HackathonSerializer(hackathon)
        return Response({'data': serializer.data})

    def put(self, request, pk, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # ✅ Require authentication for PUT
        self.check_permissions(request)

        hackathon = get_object_or_404(HackathonsList, id=pk)

        # ✅ Ensure only the creator can update the hackathon
        if hackathon.created_by != request.user:
            return Response({'error': 'You do not have permission to update this hackathon'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = HackathonSerializer(hackathon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # ✅ Require authentication for DELETE
        self.check_permissions(request)

        hackathon = get_object_or_404(HackathonsList, id=pk)

        if hackathon.created_by != request.user:
            return Response({'error': 'You do not have permission to delete this hackathon'}, status=status.HTTP_403_FORBIDDEN)
        
        hackathon.delete()
        return Response({'message': 'The Object has been deleted!'}, status=status.HTTP_204_NO_CONTENT)


class ApplyHackathonView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        print("Authenticated User:", request.user)  # ✅ Debugging output
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        hackathon = get_object_or_404(HackathonsList, id=pk)
        if not hackathon.status:
            return Response({'error': 'You can only apply for active hackathons'}, status=status.HTTP_400_BAD_REQUEST)

        if HackathonApplication.objects.filter(user=request.user, hackathon=hackathon).exists():
            return Response({'error': 'You have already applied'}, status=status.HTTP_400_BAD_REQUEST)

        HackathonApplication.objects.create(user=request.user, hackathon=hackathon)
        return Response({'message': 'Successfully applied!'}, status=status.HTTP_201_CREATED)


class HackathonApplicationsListView(generics.ListAPIView):
    queryset = HackathonApplication.objects.all()
    serializer_class = HackathonApplicationSerializer

    def get_queryset(self):
        # Optionally filter applications by hackathon_id
        hackathon_id = self.request.query_params.get('id')
        if hackathon_id:
            return HackathonApplication.objects.filter(hackathon_id=hackathon_id)
        return super().get_queryset()

