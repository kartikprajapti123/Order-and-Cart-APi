from django.contrib import admin
from django.urls import path,include
from app.views import CartView,CartItemView,OrderView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter,DefaultRouter

router=DefaultRouter()

router.register('cart',CartView,basename="cart")
router.register('order',OrderView,basename="order")



nested_router=NestedDefaultRouter(router,'cart',lookup='cart_pk')
nested_router.register('items',CartItemView,basename="Cart-detail")




urlpatterns = [
    
    path('',include(router.urls)),
    path('',include(nested_router.urls)),
    
    
]
