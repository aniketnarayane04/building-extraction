from django.db import models

# Create your models here.
class building(models.Model):
    input_image = models.ImageField(upload_to="")
    