from rest_framework import generics, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.http import Http404
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from .permissions import CanAccessMenuItems, IsManager, IsDeliveryCrew
from datetime import datetime
   
# Menu-items endpoints
class MenuItemAPIView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, CanAccessMenuItems]
    ordering_fields = ['price']
    search_fields = ['title']
    filterset_fields = ['category', 'feature']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, CanAccessMenuItems]
# End

# User group management endpoints
class ManagerListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the user already exists
        try:
            user = User.objects.get(username=username)
            created = False
        except User.DoesNotExist:
            # User does not exist, create a new one
            user = User.objects.create_user(username=username)
            created = True

        # Check if the user is already in the "Delivery crew" group
        if user.groups.filter(name='Delivery crew').exists():
            return Response({'detail': 'User is already in the Delivery crew group.'}, status=status.HTTP_400_BAD_REQUEST)


        # Assign user to the "Manager" group
        group = Group.objects.get(name='Manager')
        user.set_password(password)
        user.email = email  # Set the email value
        user.save()
        user.groups.add(group)

        # Serialize the user data
        serializer = self.get_serializer(user)
        data = serializer.data

        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response(data, status=status_code)


class ManagerUserDetailAPIView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        user = self.get_object(kwargs['pk'])
        group = Group.objects.get(name='Manager')

        if group in user.groups.all():
            user.groups.remove(group)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class DeliveryCrewListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the user already exists
        try:
            user = User.objects.get(username=username)
            created = False
        except User.DoesNotExist:
            # User does not exist, create a new one
            user = User.objects.create_user(username=username)
            created = True

        # Check if the user is already in the "Manager" group
        if user.groups.filter(name='Manager').exists():
            return Response({'detail': 'User is already in the Delivery crew group.'}, status=status.HTTP_400_BAD_REQUEST)


        # Assign user to the "Manager" group
        group = Group.objects.get(name='Delivery crew')
        user.set_password(password)
        user.email = email  # Set the email value
        user.save()
        user.groups.add(group)

        # Serialize the user data
        serializer = self.get_serializer(user)
        data = serializer.data

        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response(data, status=status_code)


class DeliveryCrewUserDetailAPIView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        user = self.get_object(kwargs['pk'])
        group = Group.objects.get(name='Delivery crew')

        if group in user.groups.all():
            user.groups.remove(group)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class CartMenuItemsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        menuitem_id = request.data.get('menuitem_id')
        quantity = request.data.get('quantity')

        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except ObjectDoesNotExist:
            return Response({"error": "MenuItem not found."}, status=404)


        menuitem = MenuItem.objects.get(id=menuitem_id)
        unit_price = menuitem.price
        price = unit_price * int(quantity)

        cart_item = Cart.objects.create(
            user=request.user,
            menuitem=menuitem,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )

        # Retrieve the user and menuitem fields for serialization
        user_username = request.user.username
        menuitem_title = menuitem.title

        # Create a dictionary with the additional fields
        additional_fields = {
            'user': user_username,
            'menuitem': menuitem_title
        }

        # Merge the additional fields with the serialized data
        serialized_data = self.serializer_class(cart_item).data
        serialized_data.update(additional_fields)

        return Response(serialized_data, status=201)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        message = "Cart Deleted Successfully"
        return Response({"message": message}, status=200)
    

class OrderCreateListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    ordering_fields = ['total', 'date']
    filterset_fields = ['status']
    

    def post(self, request, format=None):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total = 0
        order_items = []

        order = Order(
            user=user,
            delivery_crew=None,  # Set the delivery crew later if needed
            status=False,
            total=0,  # Initialize total as 0
            date=datetime.now()
        )
        order.save()

        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,  # Set the order_id field
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            total += cart_item.price
            order_items.append(order_item)

        order.total = total  # Update the total of the order
        order.save()

        OrderItem.objects.bulk_create(order_items)  # Bulk create the order items

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    

    def get(self, request, format=None):
        user = request.user

        if IsManager().has_permission(request, self):
            orders = Order.objects.all()
        elif IsDeliveryCrew().has_permission(request, self):
            orders = Order.objects.filter(delivery_crew=user)
        else:
            orders = Order.objects.filter(user=user)


        # Ordering
        ordering = request.GET.get('ordering')
        if ordering and ordering in self.ordering_fields:
            orders = orders.order_by(ordering)


        # Filter orders based on the user's role
        if IsManager().has_permission(request, self):
            status = request.GET.get('status')
            if status:
                orders = orders.filter(status=status)
        elif IsDeliveryCrew().has_permission(request, self):
            status = request.GET.get('status')
            if status:
                orders = orders.filter(status=status)
            orders = orders.filter(delivery_crew=user)
        else:
            status = request.GET.get('status')
            if status:
                orders = orders.filter(status=status)
            orders = orders.filter(user=user)

        # Filter orders by delivery_crew (null or specific username)
        delivery_crew_filter = request.GET.get('delivery_crew')
        if delivery_crew_filter:
            if delivery_crew_filter.lower() == 'null':
                orders = orders.filter(delivery_crew__isnull=True)
            else:
                orders = orders.filter(delivery_crew__username=delivery_crew_filter)

           
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_id = self.kwargs['pk']
        order = Order.objects.filter(id=order_id).prefetch_related('order_Items__menuitem').first()

        # Check if the order item exists
        if not order:
            raise Http404
        
        # Check if the order belongs to the current user (for detail view)
        if self.request.method == 'GET' and order.user != self.request.user:
            raise PermissionDenied("You don't have permission to access this order.")


        return order

    def put(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            if 'delivery_crew' in request.data:
                delivery_crew_id = request.data['delivery_crew']
                delivery_crew = User.objects.filter(id=delivery_crew_id, groups__name='Delivery crew').first()

                if delivery_crew:
                    request.data['delivery_crew'] = delivery_crew.id
                else:
                    return Response({'detail': 'Invalid delivery crew ID.'}, status=status.HTTP_400_BAD_REQUEST)

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            if 'delivery_crew' in request.data:
                delivery_crew_id = request.data['delivery_crew']
                delivery_crew = User.objects.filter(id=delivery_crew_id, groups__name='Delivery crew').first()

                if delivery_crew:
                    request.data['delivery_crew'] = delivery_crew.id
                else:
                    return Response({'detail': 'Invalid delivery crew ID.'}, status=status.HTTP_400_BAD_REQUEST)

        return self.partial_update(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        if IsManager().has_permission(request, self):
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You don't have permission to delete this order.")


