# serializers.py

# Supondo que você tenha estes serializadores no mesmo arquivo
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Room, Reservation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'location', 'capacity', 'available']


class ReservationSerializer(serializers.ModelSerializer):
    # Campo para LEITURA: exibe o objeto Room completo no GET.
    room = RoomSerializer(read_only=True)

    # Campo para ESCRITA: aceita um room_id no POST.
    # write_only=True garante que ele não aparecerá na resposta.
    # source='room' diz ao DRF para usar este valor para preencher o campo 'room' do modelo.
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True,
        label="Room ID" # Label para a interface da API
    )

    # Opcional: exibe os dados do usuário em vez do ID.
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'user',
            'room',       # Usado na resposta (GET)
            'room_id',    # Usado na requisição (POST)
            'start_time',
            'end_time',
            'created_at'
        ]
        read_only_fields = ('user',)

    def validate(self, data):
        """
        Verifica se o tempo de fim é depois do tempo de início.
        """
        # A validação agora deve verificar se 'start_time' e 'end_time' estão em 'data',
        # pois em um PATCH eles podem não estar presentes.
        if 'start_time' in data and 'end_time' in data and data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("O horário de término deve ser posterior ao de início.")
        return data