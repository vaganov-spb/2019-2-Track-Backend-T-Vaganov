from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
def enterpage(request):
    if request.method == 'GET':
        return render(request, "EnterPage.html")
    return HttpResponse(status=405)