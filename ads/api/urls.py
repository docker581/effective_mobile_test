from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import AdViewSet, ExchangeProposalViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'proposals', ExchangeProposalViewSet, 
                basename='proposal')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
