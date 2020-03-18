from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from users.models import User, Member
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


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


class GetMembers(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        result = []
        members = Member.objects.filter(chat_id=request.GET.get('chat_id')).values_list('user__id', flat=True).order_by('id')

        for i in list(members):
            result.append(User.objects.get(id=i))

        serializer = UserSerializer(result, many=True)

        return JsonResponse(serializer.data, safe=False)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'search_user':
            return UserSerializer
        if self.action == 'profile':
            return ProfileSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False)
    def search_user(self, request):
        username = request.GET.get('search', None)

        if not username:
            return Response(data='Can\'t get username param', status=status.HTTP_400_BAD_REQUEST)

        users = self.get_queryset()
        users = users.filter(username__icontains=username)

        if users.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response({'users': "Not exists"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='profile/(?P<user_id>[^/.]+)')
    def profile(self, request, user_id=None):
        users = self.get_queryset()
        try:
            user = users.get(id=user_id)
        except User.DoesNotExist:
            return Response({'user': 'Incorrect'}, status=status.HTTP_404_NOT_FOUND)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
