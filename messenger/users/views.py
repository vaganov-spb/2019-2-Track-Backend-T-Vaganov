from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from users.models import User, Member
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


@require_http_methods(["GET"])
def search_by_username(request):
    username = request.GET.get('search')
    if not username:
        return HttpResponseBadRequest("Cant get search param")
    users = User.objects.filter(username__icontains=username)
    if users.exists():
        users = users.values('id', 'username', 'first_name', 'last_name')
        return JsonResponse(list(users), safe=False, json_dumps_params={'ensure_ascii': False})
    response = JsonResponse('User not found', safe=False)
    response.status_code = 404
    return response
    # return HttpResponse(list(users))


@require_http_methods(["GET"])
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    data = {
               'id': user.id,
               'first name': user.first_name,
               'last name': user.last_name,
               'username': user.username,
               'last login': user.last_login,
               #'avatar': user.avatar,
               'date joined': user.date_joined,
    }
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["GET"])
def contact_list(request):
    user = User.objects.all()
    user = user.values('id', 'first_name', 'last_name', 'username', 'avatar')
    return JsonResponse(list(user), safe=False, json_dumps_params={'ensure_ascii': False})


'''
@require_http_methods(["GET"])
def get_id(request):
    name = request.GET.get('name', '')
    try:
        member = Member.objects.get(user__username=name, chat__topic='Group Chat')
    except Member.DoesNotExist:
        return HttpResponse(status=404)
    user = User.objects.get(username=name)
    return JsonResponse(user.id, safe=False, json_dumps_params={'ensure_ascii': False})
'''

