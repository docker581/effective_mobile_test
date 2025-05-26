from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('ads/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:pk>/edit/', views.ad_edit, name='ad_edit'),
    path('ads/<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('ads/<int:sender_pk>/propose/', views.proposal_create, name='proposal_create'),
    path('proposals/', views.proposal_list, name='proposal_list'),
]
