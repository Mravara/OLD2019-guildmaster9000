from django.db import models


class Dungeon(models.Model):
    name = models.CharField(max_length=128)
    gp_modifier = models.FloatField(default=1)

    def __str__(self):
        return self.name