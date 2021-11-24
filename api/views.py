from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import User, Candidate, Vacancy, Interview
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, CandidateSerializer, VacancySerializer, \
    InterviewSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(User.objects.filter(id=request.user.id).first()),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class UserInfoView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id).get()
        content = dict(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            company=user.company,
            gender=user.gender
        )
        return Response(content)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

