from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'author'):
            return obj.author == request.user or request.user.profile.role == 'admin'
        elif hasattr(obj, 'user'):
            return obj.user == request.user or request.user.profile.role == 'admin'
        
        return False


class IsJournalistOrAdminForCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'POST':
            return (request.user and 
                    request.user.is_authenticated and 
                    request.user.profile.role in ['jornalista', 'admin'])
        
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'author'):
            return obj.author == request.user or request.user.profile.role == 'admin'
        
        return False
