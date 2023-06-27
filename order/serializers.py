# Create a New user
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from datetime import datetime


# Get Menu Item and Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'feature', 'category', 'category_id']
# End

# Manager
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Cart
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


# Order
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source='menuitem.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'menuitem', 'quantity', 'unit_price', 'price')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    order_Items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Delivery crew'),
        allow_null=True,
        required=False
    )
    date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    delivery_crew_username = serializers.SerializerMethodField()


    def get_delivery_crew_username(self, obj):
        delivery_crew = obj.delivery_crew
        if delivery_crew is not None:
            return delivery_crew.username
        return "not assigned yet"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('delivery_crew')
        return data

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_username', 'status', 'total', 'date', 'order_Items']