from rest_framework import viewsets, filters, status, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from ..models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import AdPagination


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly,
    ]
    pagination_class = AdPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'condition']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception:
            raise NotFound(detail="Объявление не найдено")
        if ad.user != request.user:
            raise PermissionDenied(detail="Только автор может редактировать "
                                   "объявление")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception:
            raise NotFound(detail="Объявление не найдено")
        if ad.user != request.user:
            raise PermissionDenied(detail="Только автор может удалять "
                                   "объявление")
        return super().destroy(request, *args, **kwargs)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ad_sender__id', 'ad_receiver__id', 'status']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        proposal = serializer.save()
        return Response(self.get_serializer(proposal).data, 
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'status' not in request.data:
            return Response({'detail': 'Можно обновлять только статус'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            instance, 
            data={'status': request.data['status']}, 
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
