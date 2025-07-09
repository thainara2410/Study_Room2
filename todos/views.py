from rest_framework import viewsets, permissions
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from .permissions import IsAdminOrReadOnly

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que salas sejam visualizadas ou editadas.
    - Admins (is_staff=True) podem realizar CRUD completo.
    - Usuários autenticados ou anônimos podem apenas visualizar salas disponíveis.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]  # Aplica a permissão customizada

    def get_queryset(self):
        """
        Retorna todas as salas para administradores e apenas
        as disponíveis para outros usuários.
        """
        if self.request.user.is_staff:
            return Room.objects.all()
        return Room.objects.filter()


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para criar, listar, e deletar reservas.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários logados

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Associa o usuário da requisição à reserva criada."""
        serializer.save(user=self.request.user)