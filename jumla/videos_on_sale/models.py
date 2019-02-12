from django.db import models



class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=32)


class ContentEntity(models.Model):
    content_entity_id = models.AutoField(primary_key=True)
    video_pack_foreign_key = models.ForeignKey('VideoPackEntity', on_delete=models.CASCADE)
    video_foreign_key = models.ForeignKey('VideoEntity', on_delete=models.CASCADE)


class VideoEntity(models.Model):
    video_id = models.AutoField(primary_key=True)
    video_title = models.CharField(max_length=300)
    video_url = models.CharField(max_length=500)
    genre_foreign_key = models.ForeignKey('GenreEntity', on_delete=models.CASCADE)


class GenreEntity(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_title = models.CharField(max_length=100)


class VideoPackEntity(models.Model):
    video_pack_id = models.AutoField(primary_key=True)
    video_pack_name = models.CharField(max_length=100)
    video_pack_content_id = models.ForeignKey('VideosInPack', on_delete=models.CASCADE)


