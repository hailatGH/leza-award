from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':  
            return True
        return request.user.is_authenticated
