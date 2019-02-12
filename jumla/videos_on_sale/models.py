from django.db import models

class Users(models.Model):
    user_id = models.CharField(max_length=10)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=32)


    # artist = models.ForeignKey(Musician, on_delete=models.CASCADE)

