from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the authenticated user is the creator of the ticket
        return obj.created_by == request.user