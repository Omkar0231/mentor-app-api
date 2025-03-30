from django.shortcuts import render, get_object_or_404
from .models import HackathonsList
from rest_framework.views import APIView
from .serializers import HackathonSerializer, HackathonApplicationSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import HackathonsList, HackathonApplication

# Create your views here.

class HackathonsListView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = HackathonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
    def get(self, request, pk, *args, **kwargs):
        hackathon = get_object_or_404(HackathonsList, id=pk)
        serializer = HackathonSerializer(hackathon)
        return Response({'data': serializer.data})

    def put(self, request, pk, *args, **kwargs):
        hackathon = get_object_or_404(HackathonsList, id=pk)
        serializer = HackathonSerializer(hackathon, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        hackathon = get_object_or_404(HackathonsList, id=pk)
        hackathon.delete()
        return Response({'message': 'The Object has been deleted!'}, status=status.HTTP_204_NO_CONTENT)

# class ActiveHackathonsListView(generics.ListAPIView):
#     queryset = HackathonsList.objects.filter(status=True)
#     serializer_class = HackathonSerializer


class ApplyHackathonView(APIView):
    authentication_classes = [TokenAuthentication]  # ✅ Require token authentication
    permission_classes = [IsAuthenticated]  # ✅ Only authenticated users can apply

    def post(self, request, pk, *args, **kwargs):
        # self.request.user
        hackathon = get_object_or_404(HackathonsList, id=pk)

        # Check if Hackathon is inactive
        if not hackathon.status:
            return Response({'error': 'This hackathon is not active.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user  # ✅ Get user from token

        # Check if the user has already applied
        if HackathonApplication.objects.filter(hackathon=hackathon, user=user).exists():
            return Response({'error': 'You have already applied to this hackathon!'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create application with user automatically
        HackathonApplication.objects.create(hackathon=hackathon, user=user)

        return Response({'message': 'Successfully applied!'}, status=status.HTTP_201_CREATED)

        # Pass hackathon in serializer context
        serializer = HackathonApplicationSerializer(data=request.data, context={'hackathon': hackathon})
        if serializer.is_valid():
            serializer.save()  # 'hackathon' is automatically set
            return Response({'message': 'Successfully applied!'}, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HackathonApplicationsListView(generics.ListAPIView):
    queryset = HackathonApplication.objects.all()
    serializer_class = HackathonApplicationSerializer

    def get_queryset(self):
        # Optionally filter applications by hackathon_id
        hackathon_id = self.request.query_params.get('id')
        if hackathon_id:
            return HackathonApplication.objects.filter(hackathon_id=hackathon_id)
        return super().get_queryset()


        

def hackathons(request):
    hackathons_list = HackathonsList.objects.all()
    return render(request, 'hackathons/hackathons.html', {'hackathons_list': hackathons_list})

