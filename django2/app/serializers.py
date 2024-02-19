from .models import Product, Cart, CartItem, Order, OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "title", "price"]


class CartItemSerailizer(serializers.ModelSerializer):
    product = ProductSerializer()
    totalprice = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "totalprice"]

    def get_totalprice(self, cartitem: CartItem):
        return cartitem.quantity * cartitem.product.price


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerailizer(many=True, read_only=True)
    totalprice = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "totalprice"]

    def get_totalprice(self, cart: Cart):
        total = 0
        for item in cart.items.all():
            total += item.product.price * item.quantity

        return total


class AddCartItemSerailizer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        print(product_id)
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("No products are avalibale with this id")
        return attrs

    def save(self, **kwargs):
        print(self.context)
        cart_id = self.context.get("cart_id")
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        print(cart_id, product_id, quantity)
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, product_id=product_id, quantity=quantity
            )

        self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


# /////////////////////////////////////////////////////ORDER //////////////////////////////////////////////API /////////////////////////////////////////////////////////


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "payment_status", "customer", "items"]


class CreateOrderSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            print(self.validated_data["cart_id"])
            print(self.context["user_id"])

            (user, created) = User.objects.get_or_create(id=self.context["user_id"])
            orders = Order.objects.create(customer=user)

            cart_items = CartItem.objects.filter(cart_id=self.validated_data["cart_id"])

            order_items = [
                OrderItem(order=orders, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=self.validated_data["cart_id"]).delete()


    def validate(self, attrs):
        cart_id=attrs.get('cart_id')
        cart_exists=Cart.objects.filter(id=cart_id)
        print(cart_exists)
        print(cart_exists.count())
        print(cart_exists.exists())
        
        if not cart_exists.exists():
            raise serializers.ValidationError("Cart does not exists")
        
        elif CartItem.objects.filter(cart_id=cart_id).count()==0:

            raise serializers.ValidationError("cart is empty")
        return attrs
    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['payment_status']