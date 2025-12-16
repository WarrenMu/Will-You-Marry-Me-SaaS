from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProposalViewSet, health

router = DefaultRouter()
router.register(r'proposals', ProposalViewSet, basename='proposal')

urlpatterns = [
    path('health/', health),
    path('', include(router.urls)),
]
