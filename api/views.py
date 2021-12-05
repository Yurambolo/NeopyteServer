from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Candidate, Vacancy, Interview
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, CandidateSerializer, VacancySerializer, \
    InterviewSerializer, UserSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     response = Response(serializer.data)
    #     if instance.sv_file:
    #         response.
    #     return response


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
