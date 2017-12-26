from rest_framework import permissions

#Custom permission to only allow owners of content to view or edit it.
class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user and
            request.method in ['GET', 'PATCH', 'DELETE'])

#Custom permission to only allow owners of an object to edit it.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.user == request.user
