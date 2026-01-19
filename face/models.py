from django.db import models

class FaceUser(models.Model):
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=128)  # Still use hashed in production!

    def __str__(self):
        return self.email or self.phone_number
