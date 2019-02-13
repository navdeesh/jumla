from django.template import Template, Context
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

import json

from videos_on_sale.models import *

import datetime as dtt
from datetime import datetime

import pytz

utc=pytz.UTC

def index(request):
    if("logged_in" in request.session):
        return redirect('/jumla/home')
    return redirect('/jumla/login')

def do_logout(request):
    if("logged_in" in request.session):
        del request.session["logged_in"]
        del request.session["user_id"]
    return redirect('/jumla/')

    
def login(request):
    if("logged_in" in request.session):
        return redirect('/jumla/home')
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = Users.objects.get(user_email=email)
            if(user.user_password == password):
                request.session['user_id'] = user.user_id
                request.session['logged_in'] = "yes"
                return redirect('/jumla/home')
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Wrong Password'
                }, status=401)

        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'JSON parse error'
            }, status=400)

        except KeyError:
            return JsonResponse({
                'success': False,
                'message': 'Please supply email and password in request body'
            }, status=401)

        except ObjectDoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User does not exists'
            }, status=401)
    
    else:
        fp = open('templates/login.html')
        t = Template(fp.read())
        fp.close()
        html = t.render(Context({}))
        return HttpResponse(html)



def home(request):
    if(not "logged_in" in request.session):
        return redirect('/jumla/login')
    fp = open('templates/home.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({}))
    return HttpResponse(html)

def show_content(request, **kwargs):
    if request.method == "GET":
        if "logged_in" in request.session:
            video_or_videopack = kwargs['video_or_videopack']
            content_id = kwargs['content_id']
            user_id = int(request.session['user_id'])
            prices = Pricing.objects.filter(user_foreign_key=user_id).filter(content_foreign_key=content_id).first()
            ret_dict = prices.__dict__
            del ret_dict['_state']
            if(video_or_videopack == "video_pack"):
                video_pack_id = content_id
                video_pack = VideoPackEntity.objects.get(pk=video_pack_id)
                videos_array = get_videos_array(video_pack_id)
                ret_dict['type'] = 'video_pack'
                ret_dict['video_pack'] = {
                    'name': video_pack.video_pack_name,
                    'videos': videos_array
                }
            else:
                video_id = content_id
                video = VideoEntity.objects.get(pk=video_id).__dict__
                del video['_state']
                ret_dict['type'] = 'video'
                ret_dict['video'] = video
            for key, value in ret_dict.items() :
                print (key)
            fp = open('templates/show_content.html')
            t = Template(fp.read())
            fp.close()
            html = t.render(Context({"back_data": ret_dict}))
            return HttpResponse(html)
        else:
            return redirect("/jumla/")
    else:
        return redirect("/jumla/")

def sign_in(request):
    if request.method == "POST":
        try:
            request_body=json.loads(request.body)
            email = request_body['email']
            password = request_body['password']
            user = Users.objects.get(user_email=email)
            if(user.user_password == password):
                request.session['user_id'] = user.user_id
                request.session['logged_in'] = "yes"
                return JsonResponse({
                    'success': True,
                    'message': 'Login Successful'
                }, status=200)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Wrong Password'
                }, status=401)

        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'JSON parse error'
            }, status=400)

        except KeyError:
            return JsonResponse({
                'success': False,
                'message': 'Please supply email and password in request body'
            }, status=401)

        except ObjectDoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User does not exists'
            }, status=401)
    
    else:
        return JsonResponse({
            'success': False,
            'message': 'Only post requests allowed'
        }, status=405)



def logout(request):
    if("logged_in" in request.session):
        del request.session["logged_in"]
        del request.session["user_id"]
        return JsonResponse({
            'success': True,
            'message': 'Successfully logged out'            
        }, status=200)
    else:
        return JsonResponse({
            'success': False,
            'message': 'You are not logged in'
        }, status=401)



def get_videos_array(video_pack_id):
    arr = VideosInPack.objects.filter(video_pack_entity_foreign_key=video_pack_id)
    ret_array = []
    for a in arr:
        a = a.__dict__
        video_id = a['video_entity_foreign_key_id']
        video = VideoEntity.objects.get(pk=video_id).__dict__
        del video['_state']
        ret_array.append(video)
    return ret_array


def get_content(request):
    if request.method == "GET":
        if "logged_in" in request.session:
            user_id = int(request.session['user_id'])
            prices = Pricing.objects.filter(user_foreign_key=user_id)
            response_array = []
            for price in prices:
                price = price.__dict__
                del price['_state']
                content_foreign_key_id = price['content_foreign_key_id']
                content = ContentEntity.objects.get(pk=content_foreign_key_id)
                if content.video_pack_foreign_key:
                    video_pack_id = content.__dict__['video_pack_foreign_key_id']
                    video_pack = VideoPackEntity.objects.get(pk=video_pack_id)
                    videos_array = get_videos_array(video_pack_id)
                    price['type'] = 'video_pack'
                    price['video_pack'] = {
                        'name': video_pack.video_pack_name,
                        'videos': videos_array
                    }
                else:
                    video_id = content.__dict__['video_foreign_key_id']
                    video = VideoEntity.objects.get(pk=video_id).__dict__
                    del video['_state']
                    price['type'] = 'video'
                    price['video'] = video
                response_array.append(price)
            return JsonResponse({
                'success': True,
                'message': 'Successfully fetched the content',
                'data': response_array,
                'generes_array': ['', 'Action', 'Absurdist', 'Adventure', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Historical', 'Historical fiction', 'Horror', 'Magical realism', 'Mystery', 'Paranoid Fiction', 'Philosophical', 'Political', 'Romance', 'Saga', 'Satire', 'Science fiction', 'Social', 'Speculative', 'Thriller', 'Urban', 'Western']
            }, status=200)

        else:
            return JsonResponse({
                'success': False,
                'message': 'You need to login first'
            }, status=401)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Only get requests allowed'
        }, status=405)

def get_subscribed_amount(content_id, user_id, duration):
    Pricing.objects.filter(user_foreign_key=user_id).filter(content_foreign_key=content_id)
    _dict = Pricing.objects.filter(user_foreign_key=user_id).filter(content_foreign_key=content_id).first().__dict__
    if(duration == 'daily'):
        return _dict['pricing_daily_basis']
    elif(duration == 'weekly'):
        return _dict['pricing_weekly_basis']
    elif(duration == 'monthly'):
        return _dict['pricing_monthly_basis']
    else:
        return _dict['pricing_yearly_basis']

def my_subscriptions_page(request):
    if(not "logged_in" in request.session):
        return redirect('/jumla/login')
    fp = open('templates/my_subscriptions_page.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({}))
    return HttpResponse(html)

def subscribe(request):
    if request.method == "POST":
        
        if "logged_in" in request.session:
            
            user_id = int(request.session['user_id'])
            
            try:
                content_id = int(request.POST.get('content_id'))
                duration = request.POST.get('duration')
                subscribed_amount = get_subscribed_amount(content_id, user_id, duration)
                Subscribed(
                    user_foreign_key = Users.objects.get(pk=user_id),
                    content_foreign_key = ContentEntity.objects.get(pk=content_id),
                    subscribed_amount = subscribed_amount,
                    subscribed_duration = duration
                ).save()
                
                return redirect("/jumla/my_subscriptions_page")
            
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'JSON parse error'
                }, status=400)
            
            except KeyError:
                return JsonResponse({
                    'success': False,
                    'message': 'Please supply email and password in request body'
                }, status=401)

            except ObjectDoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User does not exists'
                }, status=401)
            
            except:
                return JsonResponse({
                    'success': False,
                    'message': 'Unknown error'
                }, status=500)
        
        else:
            
            return JsonResponse({
                'success': False,
                'message': 'You need to login first'
            }, status=401)
    
    else:
        
        return JsonResponse({
            'success': False,
            'message': 'Only post requests allowed'
        }, status=405)


def get_content_by_id(content_foreign_key):
    content = ContentEntity.objects.get(pk=content_foreign_key)
    if content.video_pack_foreign_key:
        video_pack_id = content.__dict__['video_pack_foreign_key_id']
        video_pack = VideoPackEntity.objects.get(pk=video_pack_id)
        videos_array = get_videos_array(video_pack_id)
        ret_dict = {}
        ret_dict['type'] = 'video_pack'
        ret_dict['video_pack'] = {
            'name': video_pack.video_pack_name,
            'videos': videos_array
        }
    else:
        video_id = content.__dict__['video_foreign_key_id']
        video = VideoEntity.objects.get(pk=video_id).__dict__
        del video['_state']
        ret_dict = {}
        ret_dict['type'] = 'video'
        ret_dict['video'] = video
    return ret_dict
    

def my_subscriptions(request):
    if request.method == "GET":
        
        if "logged_in" in request.session:
            
            user_id = int(request.session['user_id'])
            subscriptions = Subscribed.objects.filter(user_foreign_key=user_id)
            ret_array = []
            for s in subscriptions:
                s = s.__dict__
                del s['_state']
                content_foreign_key = s['content_foreign_key_id']
                s['content'] = get_content_by_id(content_foreign_key)
                s['is_expired'] = is_subscription_expired(s)
                ret_array.append(s)
            return JsonResponse({
                'success': True,
                'message': 'Success',
                'data': ret_array
            }, status=200)
        else:
            
            return JsonResponse({
                'success': False,
                'message': 'You need to login first'
            }, status=401)
    
    else:
        
        return JsonResponse({
            'success': False,
            'message': 'Only get requests allowed'
        }, status=405)



def get_add_ons(request, **kwargs):
    if request.method == "GET":

        if "logged_in" in request.session:
            
            subscribed_content_id = kwargs['id']
            duration = kwargs['duration']
            add_ons = AddOns.objects.filter(addons_for_content_id=subscribed_content_id).filter(addon_duration=duration)
            ret_array = []
            for a in add_ons:
                a = a.__dict__
                if a['addons_content_id'] != subscribed_content_id:
                    del a['_state']
                    a['content'] = get_content_by_id(a['addons_content_id'])
                    ret_array.append(a)
            
            return JsonResponse({
                'success': True,
                'message': 'Success',
                'data': ret_array
            }, status=200)


    else:

        return JsonResponse({
            'success': False,
            'message': 'Only GET requests allowed'
        }, status=405)



def view_content(request, **kwargs):
    if request.method == "GET":
        if "logged_in" in request.session:
            video_or_videopack = kwargs['video_or_videopack']
            content_id = kwargs['content_id']
            user_id = int(request.session['user_id'])
            prices = Pricing.objects.filter(user_foreign_key=user_id).filter(content_foreign_key=content_id).first()
            ret_dict = prices.__dict__
            del ret_dict['_state']
            if(video_or_videopack == "video_pack"):
                video_pack_id = content_id
                video_pack = VideoPackEntity.objects.get(pk=video_pack_id)
                videos_array = get_videos_array(video_pack_id)
                ret_dict['type'] = 'video_pack'
                ret_dict['video_pack'] = {
                    'name': video_pack.video_pack_name,
                    'videos': videos_array
                }
            else:
                video_id = content_id
                video = VideoEntity.objects.get(pk=video_id).__dict__
                del video['_state']
                ret_dict['type'] = 'video'
                ret_dict['video'] = video
            for key, value in ret_dict.items() :
                print (key)
            fp = open('templates/view_content.html')
            t = Template(fp.read())
            fp.close()
            html = t.render(Context({"back_data": ret_dict}))
            return HttpResponse(html)
        else:
            return redirect("/jumla/")
    else:
        return redirect("/jumla/")

def is_subscription_expired(self):
    if(str.lower(self['subscribed_duration'])== "daily" and (self['subscribed_start_date']) < utc.localize(datetime.now()) < ((self['subscribed_start_date']) + dtt.timedelta(days=1) )):
        return False
    elif (str.lower(self['subscribed_duration'])== "weekly" and (self['subscribed_start_date']) < utc.localize(datetime.now()) < ((self['subscribed_start_date']) + dtt.timedelta(days=7) )):
        return False
    elif (str.lower(self['subscribed_duration']) == "month" and (self['subscribed_start_date']) < utc.localize(datetime.now()) < ((self['subscribed_start_date']) + dtt.timedelta(days=30) )):
        return False
    elif (str.lower(self['subscribed_duration']) == "yearly" and (self['subscribed_start_date']) < utc.localize(datetime.now()) < ((self['subscribed_start_date']) + dtt.timedelta(days=365) )):
        return False
    else:
        return True


