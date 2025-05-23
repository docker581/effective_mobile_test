from rest_framework import viewsets, permissions, filters, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly,
    ]

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
    search_fields = ['status', 'ad_sender__id', 'ad_receiver__id']

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
