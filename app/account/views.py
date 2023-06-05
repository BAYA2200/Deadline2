from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from .decorators import login_required
from .models import User, Profile
from .serializers import RegisterSerializer, ProfileSerializer


class RegisterView(CreateAPIView):
    """
    Blog API endpoint to get list of blogs and create blogs
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProfileListCreateView(ListCreateAPIView):
    """
    Forum API endpoint to get list of blogs and create forum
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [BasePermission, IsAuthenticated]

    @login_required
    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Forum API endpoint to retrieve, update and delete forum
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [BasePermission, IsAuthenticated]
