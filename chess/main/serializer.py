from rest_framework import serializers
from .models import ChessGame

class ChessGameSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChessGame
        fields=('current_player_turn','fields_chess', 'winner_player', 'started_at')


class ChessGameSerializerPost(serializers.ModelSerializer):
    class Meta:
        model=ChessGame
        fields=()

