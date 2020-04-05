from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import jwt
from django.conf import settings

# Create your views here.
def enterpage(request):
    if request.method == 'GET':
        return render(request, "EnterPage.html")
    return HttpResponse(status=405)


def centrifugo_token(request):
    claims = {"sub": str(request.GET.get('user_id'))}
    print(claims)
    token = jwt.encode(claims, settings.CENTRIFUGE_SECRET, algorithm="HS256").decode()
    return JsonResponse({'token': token})
