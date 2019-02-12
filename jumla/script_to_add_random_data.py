import random
from videos_on_sale.models import *
import time


domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = ["a", "b", "c", "d","e", "f", "g", "h", "i", "j", "k", "l"]
genre_arr = ['Action', 'Absurdist', 'Adventure', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Historical', 'Historical fiction', 'Horror', 'Magical realism', 'Mystery', 'Paranoid Fiction', 'Philosophical', 'Political', 'Romance', 'Saga', 'Satire', 'Science fiction', 'Social', 'Speculative', 'Thriller', 'Urban', 'Western']
Duration = ['weekly', 'daily', 'monthly', 'yearly']

######### For User ########

def getName():
    email_name = ""
    for i in range(7):
        email_name = email_name + letters[random.randint(0, 11)]
    return email_name



def get_one_random_domain(domains):
    return random.choice(domains)

def get_one_random_name(letters):
    email_name = ""
    for i in range(7):
        email_name = email_name + letters[random.randint(0,11)]
    return email_name


def generate_random_emails():
         one_name = str(get_one_random_name(letters))
         one_domain = str(get_one_random_domain(domains))
         return one_name  + "@" + one_domain

for x in range(1,100):
    user = Users(user_id=x+100, user_name=getName(), user_email=generate_random_emails(),user_password="password")
    user.save()


######## for GenreEntity #######

for x in range(len(genre_arr)):
    genre = GenreEntity(genre_id=x+1, genre_title=genre_arr[x])
    genre.save()



###### VideoPackEntity ######

def random_name_videopack(letters):
        pack_name = ""
        for i in range(7):
            pack_name = pack_name + letters[random.randint(0, 11)]
        return pack_name

for x in range(1,100):
    videoPack = VideoPackEntity(video_pack_id=x+100, video_pack_name=random_name_videopack(letters))
    videoPack.save()



##### VideoEntity####
def random_video_title(letters):
    title = ""
    for i in range(7):
        title = title + letters[random.randint(0,11)]
    return title


for x in range(1, 100):
    videos = VideoEntity(
        video_id=x+100,
        video_title=random_video_title(letters),
        video_url= "TgT3lSZcB4s",
        genre_foreign_key=GenreEntity.objects.get(pk=random.randint(1, 20))
    )
    videos.save()


######## VideosInPack #####

for x in range(1, 100):
    videosInPack = VideosInPack(videos_in_pack_id=x + 100, video_entity_foreign_key=VideoEntity.objects.get(pk=random.randint(102, 199)),
                                  video_pack_entity_foreign_key=VideoPackEntity.objects.get(pk=random.randint(102, 199)))
    videosInPack.save()


############# ContentEntity ######

for x in range(101, 200, 2):
    contentEntity = ContentEntity(content_entity_id=x, video_pack_foreign_key = VideoPackEntity.objects.get(pk=random.randint(102, 199)))
    contentEntity.save()
    contentEntity = ContentEntity(content_entity_id=x+1, video_foreign_key=VideoEntity.objects.get(pk=random.randint(102, 199)))
    contentEntity.save()                              



#####  Pricing ######
print("Creating pricing table, it will take some time")

for x in range(1, 5000):
    pricing = Pricing(user_foreign_key = Users.objects.get(pk=random.randint(102, 198)),
        content_foreign_key = ContentEntity.objects.get(pk=random.randint(102, 198)),
        pricing_daily_basis = random.randint(1, 100) * 10,
        pricing_weekly_basis = random.randint(1, 100) * 10,
        pricing_monthly_basis = random.randint(1, 50) * 100,
        pricing_yearly_basis = random.randint(1, 20) * 1000
    )
    pricing.save()



######## Addons #########
print("Creating AddOns table, it will take some time")

for x in range(1, 5000):
    addOn = AddOns(
        addons_for_content_id = ContentEntity.objects.get(pk=random.randint(102, 198)),
        addons_content_id = random.randint(102, 198),
        addon_price = random.randint(1, 50)*100,
        addon_duration=random.choice(Duration)
    )
    addOn.save()






