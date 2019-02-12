from django.db import models
import datetime


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=32)


class ContentEntity(models.Model):
    content_entity_id = models.AutoField(primary_key=True)
    video_pack_foreign_key = models.ForeignKey('VideoPackEntity', on_delete=models.CASCADE, null=True, blank=True)
    video_foreign_key = models.ForeignKey('VideoEntity', on_delete=models.CASCADE, null=True, blank=True)


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

class VideosInPack(models.Model):
    videos_in_pack_id = models.AutoField(primary_key=True)
    video_entity_foreign_key = models.ForeignKey('VideoEntity', on_delete=models.CASCADE)
    video_pack_entity_foreign_key = models.ForeignKey('VideoPackEntity', on_delete=models.CASCADE)


class Pricing(models.Model):
    user_foreign_key = models.ForeignKey('Users', on_delete=models.CASCADE)
    content_foreign_key = models.ForeignKey('ContentEntity', on_delete=models.CASCADE)
    pricing_daily_basis = models.IntegerField();
    pricing_weekly_basis = models.IntegerField();
    pricing_monthly_basis = models.IntegerField();
    pricing_yearly_basis = models.IntegerField();


class Subscribed(models.Model):
    subscribed_id = models.AutoField(primary_key=True)
    user_foreign_key = models.ForeignKey('Users', on_delete=models.CASCADE)
    content_foreign_key = models.ForeignKey('ContentEntity', on_delete=models.CASCADE)
    subscribed_amount = models.IntegerField()
    subscribed_duration = models.CharField(max_length=10)
    subscribed_start_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def is_subscription_expired(self):
        if(str.lower(self.subscribed_duration)== "daily" and
                self.subscribed_start_date < datetime.now() < (self.subscribed_start_date + datetime.timedelta(days=1)
                )):
            return True
        elif (str.lower(self.subscribed_duration)== "weekly" and
                self.subscribed_start_date < datetime.now() < (self.subscribed_start_date + datetime.timedelta(days=7)
                )):
            return True
        elif (str.lower(self.subscribed_duration) == "month" and
              self.subscribed_start_date < datetime.now() < (self.subscribed_start_date + datetime.timedelta(days=30)
              )):
            return True
        elif (str.lower(self.subscribed_duration) == "yearly" and
              self.subscribed_start_date < datetime.now() < (self.subscribed_start_date + datetime.timedelta(days=365)
              )):
            return True
        else:
            return False

class AddOns(models.Model):
    addons_for_content_id = models.ForeignKey('ContentEntity', on_delete=models.CASCADE)
    addons_content_id = models.IntegerField();
    addon_price = models.IntegerField();
    addon_duration = models.CharField(max_length=10);
