from django.db import models

from django.contrib.auth.models import User

class Cosmiatra(User):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    escosmiatra = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.escosmiatra = True
        super(Cosmiatra, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


# Create your models here.
