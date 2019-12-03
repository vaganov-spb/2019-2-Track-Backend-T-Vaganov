from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from users.models import User, Member
from chats.models import Chat, Message
from django.views.decorators.http import require_http_methods
from chats.forms import ChatForm, MessageForm, AttachmentForm


@require_http_methods(["GET"])
def chats(request, user_id):
    chats_list = Member.objects.filter(user_id=user_id)
    chats_list = chats_list.values('chat_id',
                                   'last_read_message__content',
                                   'last_read_message__added_at',
                                   'chat__topic',
                                   'user__avatar')
    chats_list = chats_list.order_by('last_read_message__added_at')
    return JsonResponse(
        list(chats_list),
        safe=False,
        json_dumps_params={'ensure_ascii': False}
    )
    # return HttpResponse(list(chats_list))


@require_http_methods(["POST"])
def create_chat(request, user_id):
    form = ChatForm(request.POST, user_id=user_id)
    if form.is_valid():
        chat = form.save()
        member = Member.objects.create(user_id=user_id, chat=chat)
        return JsonResponse({
            'status': 'Чат создан',
            'id': chat.id
        })
    return JsonResponse({'errors': form.errors}, status=400)


@require_http_methods(["GET"])
def message_list(request, user_id):
    chat_id = request.GET.get('chatId')
    if not chat_id:
        return HttpResponseBadRequest("Cant get chat_id param")
    user_chat = get_object_or_404(Member, chat_id=chat_id, user_id=user_id)
    chat = Message.objects.filter(chat_id=chat_id).order_by('added_at')
    chat = chat.values('chat_id', 'added_at', 'content', 'user_id', 'chat__topic', 'chat__is_group_chat')
    return JsonResponse(
        list(chat),
        safe=False,
        json_dumps_params={'ensure_ascii': False}
    )
    # return HttpResponse(list(chat))


@require_http_methods(["POST"])
def send_message(request, user_id):
    form = MessageForm(request.POST, user_id=user_id)
    if form.is_valid():
        message = form.save()
        return JsonResponse('OK', safe=False)
        # return HttpResponse(list(lat_mes))
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@require_http_methods(["POST"])
def read_mess(request, user_id, chat_id):
    user_chat = get_object_or_404(Member, chat_id=chat_id, user_id=user_id)
    message = Message.objects.filter(chat_id=chat_id).filter(user_id=user_id).latest('added_at')
    user_chat.new_messages = False
    user_chat.last_read_message = message
    user_chat.save()
    return JsonResponse('OK', safe=False)


@require_http_methods(["GET"])
def particular_chat(request, user_id, chat_id):
    member = get_object_or_404(Member, user_id=user_id, chat_id=chat_id)
    chat = get_object_or_404(Chat, id=chat_id)
    data = {
        'id': chat.id,
        'topic': chat.topic,
        'is group': chat.is_group_chat,
        'last message': chat.last_message,
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["POST"])
def attachment_save(request, user_id):
    form = AttachmentForm(request.POST, request.FILES, user_id=user_id)
    if form.is_valid():
        form.save()
    return JsonResponse('OK', safe=False)


