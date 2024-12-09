from django.db import models


class ChessGame(models.Model):
    game_code = models.CharField(max_length=5)
    player_1_code = models.CharField(max_length=10)
    player_2_code = models.CharField(max_length=10)
    fields_chess = models.JSONField()
    current_player_turn = models.IntegerField()
    winner_player = models.IntegerField()
    started_at = models.DateTimeField(auto_created=True)

    def init_fields(self):
        columns = "abcdefgh"
        self.fields_chess = {
         "1": {
            "a": {"figure": True, "owner": "white", "type": "rook"},
            "b": {"figure": True, "owner": "white", "type": "knight"},
            "c": {"figure": True, "owner": "white", "type": "bishop"},
            "d": {"figure": True, "owner": "white", "type": "queen"},
            "e": {"figure": True, "owner": "white", "type": "king"},
            "f": {"figure": True, "owner": "white", "type": "bishop"},
            "g": {"figure": True, "owner": "white", "type": "knight"},
            "h": {"figure": True, "owner": "white", "type": "rook"}
        },
        "2": {
            "a": {"figure": True, "owner": "white", "type": "pawn"},
            "b": {"figure": True, "owner": "white", "type": "pawn"},
            "c": {"figure": True, "owner": "white", "type": "pawn"},
            "d": {"figure": True, "owner": "white", "type": "pawn"},
            "e": {"figure": True, "owner": "white", "type": "pawn"},
            "f": {"figure": True, "owner": "white", "type": "pawn"},
            "g": {"figure": True, "owner": "white", "type": "pawn"},
            "h": {"figure": True, "owner": "white", "type": "pawn"}
        },
        "3": {
            "a": {"figure": False, "owner": None, "type": None},
            "b": {"figure": False, "owner": None, "type": None},
            "c": {"figure": False, "owner": None, "type": None},
            "d": {"figure": False, "owner": None, "type": None},
            "e": {"figure": False, "owner": None, "type": None},
            "f": {"figure": False, "owner": None, "type": None},
            "g": {"figure": False, "owner": None, "type": None},
            "h": {"figure": False, "owner": None, "type": None}
        },
        "4": {
            "a": {"figure": False, "owner": None, "type": None},
            "b": {"figure": False, "owner": None, "type": None},
            "c": {"figure": False, "owner": None, "type": None},
            "d": {"figure": False, "owner": None, "type": None},
            "e": {"figure": False, "owner": None, "type": None},
            "f": {"figure": False, "owner": None, "type": None},
            "g": {"figure": False, "owner": None, "type": None},
            "h": {"figure": False, "owner": None, "type": None}
        },
        "5": {
            "a": {"figure": False, "owner": None, "type": None},
            "b": {"figure": False, "owner": None, "type": None},
            "c": {"figure": False, "owner": None, "type": None},
            "d": {"figure": False, "owner": None, "type": None},
            "e": {"figure": False, "owner": None, "type": None},
            "f": {"figure": False, "owner": None, "type": None},
            "g": {"figure": False, "owner": None, "type": None},
            "h": {"figure": False, "owner": None, "type": None}
        },
        "6": {
            "a": {"figure": False, "owner": None, "type": None},
            "b": {"figure": False, "owner": None, "type": None},
            "c": {"figure": False, "owner": None, "type": None},
            "d": {"figure": False, "owner": None, "type": None},
            "e": {"figure": False, "owner": None, "type": None},
            "f": {"figure": False, "owner": None, "type": None},
            "g": {"figure": False, "owner": None, "type": None},
            "h": {"figure": False, "owner": None, "type": None}
        },
        "7": {
            "a": {"figure": True, "owner": "black", "type": "pawn"},
            "b": {"figure": True, "owner": "black", "type": "pawn"},
            "c": {"figure": True, "owner": "black", "type": "pawn"},
            "d": {"figure": True, "owner": "black", "type": "pawn"},
            "e": {"figure": True, "owner": "black", "type": "pawn"},
            "f": {"figure": True, "owner": "black", "type": "pawn"},
            "g": {"figure": True, "owner": "black", "type": "pawn"},
            "h": {"figure": True, "owner": "black", "type": "pawn"}
        },
        "8": {
            "a": {"figure": True, "owner": "black", "type": "rook"},
            "b": {"figure": True, "owner": "black", "type": "knight"},
            "c": {"figure": True, "owner": "black", "type": "bishop"},
            "d": {"figure": True, "owner": "black", "type": "queen"},
            "e": {"figure": True, "owner": "black", "type": "king"},
            "f": {"figure": True, "owner": "black", "type": "bishop"},
            "g": {"figure": True, "owner": "black", "type": "knight"},
            "h": {"figure": True, "owner": "black", "type": "rook"}
        }
    }


    def save(self, *args, **kwargs):
        if not self.pk:
            self.init_fields()
        super().save(*args, **kwargs)

