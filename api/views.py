import base64
import json
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
from django.http import HttpResponseBadRequest
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from NeopyteServer.settings import EMOTION_ANALYZER
from .models import User, Candidate, Vacancy, Interview, InterviewProgress
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


class InterviewAnalyzeView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, interview_id=None):
        request_data = request.data
        if not ("image" in request_data):
            return HttpResponseBadRequest()
        image = request_data['image']
        w = request_data['width']
        h = request_data['height']
        jpg_original = base64.b64decode(image)
        # with open("imageToSave.png", "wb") as fh:
        #     fh.write(jpg_original)
        decoded = cv2.imdecode(np.fromstring(jpg_original, np.uint8), -1)
        res = EMOTION_ANALYZER.predict(decoded)
        print(res)
        res = list(res)
        res[0] = int(res[0])
        res = json.dumps(res)
        interview_progress = InterviewProgress(
            interview_id=interview_id,
            datetime=datetime.now(),
            result=res
        )
        interview_progress.save()
        return Response()


class InterviewResultView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, interview_id=None):
        interview_progresses = InterviewProgress.objects.filter(interview_id=interview_id)
        content = dict()
        if interview_progresses:
            df = pd.DataFrame()
            emotions = [json.loads(i.result) for i in interview_progresses]
            data = pd.DataFrame(emotions)
            res = data.groupby(1).count()
            emotion_persent = res / len(data)
            content = emotion_persent.to_dict()[0]
        return Response(content)
