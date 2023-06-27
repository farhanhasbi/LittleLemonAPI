# urls.py
from django.urls import path
from .views import (
    MenuItemAPIView,
    MenuItemDetailAPIView,
    ManagerListAPIView,
    ManagerUserDetailAPIView,
    DeliveryCrewListAPIView,
    DeliveryCrewUserDetailAPIView,
    CartMenuItemsAPIView,
    OrderCreateListAPIView,
    OrderDetailAPIView
) 


urlpatterns = [
    path('api/menu-items/', MenuItemAPIView.as_view(), name='menu-item-list'),
    path('api/menu-items/<int:pk>/', MenuItemDetailAPIView.as_view(), name='menu-item-detail'),
    path('api/groups/manager/users/', ManagerListAPIView.as_view(), name='manager-list'),
    path('api/groups/manager/users/<int:pk>/', ManagerUserDetailAPIView.as_view(), name='manager-user-detail'),
    path('api/groups/delivery-crew/users/', DeliveryCrewListAPIView.as_view(), name='delivery-crew-list'),
    path('api/groups/delivery-crew/users/<int:pk>/', DeliveryCrewUserDetailAPIView.as_view(), name='delivery-crew-user-detail'),
    path('api/cart/menu-items/', CartMenuItemsAPIView.as_view(), name='cart-menu-items'),
    path('api/orders/', OrderCreateListAPIView.as_view(), name='order-create-list'),
    path('api/orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail')
]