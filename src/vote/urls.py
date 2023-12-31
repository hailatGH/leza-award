from rest_framework import routers
from django.urls import path, include
from .views import CategoryViewSet, CandidateViewSet, VoteViewSet, CategoryNoCandidateViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'category', CategoryViewSet)
router.register(r'categoryNoCandidate', CategoryNoCandidateViewSet)
router.register(r'candidate', CandidateViewSet)
router.register(r'vote', VoteViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]