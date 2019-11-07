from django.http import JsonResponse, HttpResponse


# Create your views here.

def chat_list(request, user_id):
    if request.method == 'GET':
        return JsonResponse({'Your Chat-list': '{}'.format(user_id)})
    return HttpResponse(status=405)

def particular_chat(request, user_id, chat_id):
    if request.method == 'GET':
        return JsonResponse({'Your Chat Number': '{}'.format(chat_id),
                            'Your Chat List': '{}'.format(user_id)
                             })
    return HttpResponse(status=405)




