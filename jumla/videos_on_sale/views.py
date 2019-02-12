from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sign_in(request):
    if request.method == "POST":
        return JsonResponse({
            'success': True,
            'message': 'Success'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Only post requests allowed'
        })

