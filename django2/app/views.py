from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from .models import Cart,CartItem,Product,Order,OrderItem
from .serializers import CartSerializer,CartItemSerailizer,AddCartItemSerailizer,UpdateCartItemSerializer,UpdateOrderSerializer,OrderSerializer,OrderItemSerializer,CreateOrderSerializer
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class CartView(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer
    
class CartItemView(ModelViewSet):
    http_method_names=['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method=="POST":
            print("post")
            return AddCartItemSerailizer
        
        elif self.request.method=="PATCH":
            return UpdateCartItemSerializer
        return CartItemSerailizer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk_pk']}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk_pk'])
    
    
# //////////////////////////////ORDER_VIEW///////////////////////////////////////////////////////////

class OrderView(ModelViewSet):
    
    http_method_names=['get','patch','post','delete','head','options']
    def get_permissions(self):
        if self.request.method in ['PATCH',"DELETE"]:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]
    def get_serializer_class(self):
        if self.request.method=="POST":
            return CreateOrderSerializer
        
        if self.request.method=="PATCH":
            return UpdateOrderSerializer
        
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        
        

        (user_id,created)=User.objects.get_or_create(pk=self.request.user.id)
        return Order.objects.filter(customer_id=user_id)
    
    
    
class OrderItemView(ModelViewSet):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer