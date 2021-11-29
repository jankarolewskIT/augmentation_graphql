from django.db import models


class Image(models.Model):
    base64 = models.TextField()
    path = models.ImageField(upload_to='images')




