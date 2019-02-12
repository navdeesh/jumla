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
                return JsonResponse({
                    'success': True,
                    'message': 'Login Successful'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Wrong Password'
                })
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'JSON parse error'
            })
        except KeyError:
            return JsonResponse({
                'success': False,
                'message': 'Please supply email and password in request body'
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User does not exists'
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Only post requests allowed'
        })

