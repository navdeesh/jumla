from django.http import HttpResponse, JsonResponse

import json

from videos_on_sale.models import Users



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sign_in(request):
    if request.method == "POST":
        request_body=json.loads(request.body)
        email = request_body['email']
        password = request_body['password']
        user = Users.objects.get(user_email=email)
        return JsonResponse({
            'success': True,
            'message': 'Success'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Only post requests allowed'
        })

