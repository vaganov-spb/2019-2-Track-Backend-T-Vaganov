from django.http import JsonResponse, HttpResponse

# Create your views here.
def profile(request, user_id):
        if request.method == 'GET':
                return JsonResponse({'Your ID': '{}'.format(user_id)})
        return HttpResponse(status=405)

def contact_list(request, user_id):
        if request.method == 'GET':
                return JsonResponse({'Your Contact List': '{}'.format(user_id)})
        return HttpResponse(status=405)


