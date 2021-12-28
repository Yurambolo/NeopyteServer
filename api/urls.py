from django.urls import path, include
from rest_framework import routers

from .views import MyObtainTokenPairView, RegisterView, UserViewSet, CandidateViewSet, VacancyViewSet, InterviewViewSet, \
    UserInfoView, InterviewAnalyzeView, InterviewResultView
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'interviews', InterviewViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('user/info/', UserInfoView.as_view()),
    path('', include(router.urls)),
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
    path('interviews/<int:interview_id>/analyze/', InterviewAnalyzeView.as_view()),
    path('interviews/<int:interview_id>/result/', InterviewResultView.as_view()),
]