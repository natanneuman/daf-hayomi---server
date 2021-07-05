from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('studyplan', StudyPlanViewSet, basename="studyplan")
router.register('user', CurrentUserViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('upload_daf_data', StudyPlanBackup.as_view()),
    path('daf/', DafLearnedView.as_view()),
    path('daf/<int:pk>/', DafLearnedDetailView.as_view()),
]
