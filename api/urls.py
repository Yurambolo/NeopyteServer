from django.urls import path, include
from rest_framework import routers

from .views import MyObtainTokenPairView, RegisterView, ExampleView, CandidateViewSet, VacancyViewSet, InterviewViewSet
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = [
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('test/', ExampleView.as_view()),
    path('', include(router.urls)),
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
]