from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import json

from videos_on_sale.models import Users



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
















