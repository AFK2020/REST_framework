from rest_framework import permissions
from rest.enum import RoleChoice


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            if request.user.is_authenticated:
                return (request.user.profile.role == RoleChoice.MANAGER.value)
        
        return False