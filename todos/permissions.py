# core/permissions.py

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir acesso de leitura a qualquer usuário,
    mas apenas permitir escrita para usuários administradores (is_staff).
    """
    def has_permission(self, request, view):
        # Permite métodos seguros (GET, HEAD, OPTIONS) para qualquer requisição.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permite métodos de escrita (POST, PUT, DELETE) apenas se o usuário for staff.
        return request.user and request.user.is_staff