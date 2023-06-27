from rest_framework.permissions import BasePermission, SAFE_METHODS

class CanAccessMenuItems(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name='Manager').exists():
            return True
        elif user.groups.filter(name='Delivery crew').exists() and request.method in SAFE_METHODS:
            return True
        elif not user.groups.exists() and request.method in SAFE_METHODS:
            return True
        return False
    

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
    

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.exists()
    
    
class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Delivery crew').exists()





