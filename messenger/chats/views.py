from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from application import settings
import boto3
from users.models import User, Member
from chats.models import Chat, Message, Attachment
from django.views.decorators.http import require_http_methods
from chats.forms import ChatForm, MessageForm, AttachmentForm
from rest_framework import viewsets, status
from .serializers import MemberSerializer, ChatSerializer, NewChatSerializer, MessageListSerializer, NewMessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


@require_http_methods(["GET"])
def chats(request, user_id):
    chats_list = Member.objects.filter(user_id=user_id)
    if chats_list.exists():
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
    else:
        return HttpResponse(status=404)


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
    data = []
    chat_id = request.GET.get('chatId')
    if not chat_id:
        return HttpResponseBadRequest("Cant get chat_id param")
    member_of_chat = get_object_or_404(Member, chat_id=chat_id, user_id=user_id)
    chat_messages = Message.objects.filter(chat_id=chat_id).order_by('added_at')
    if request.GET.get('new') == 'yes':
        last = member_of_chat.last_read_message.id
        chat_messages = chat_messages.filter(id__gt=last)
    # for message in chat.messages:
    for message in chat_messages:
        data.append({
            'time': message.added_at,
            'text': message.content,
            'user': message.user.username,
        })
        member_of_chat.last_read_message = chat_messages.latest('added_at')
        member_of_chat.save(update_fields=["last_read_message"])
    return JsonResponse(
        data,
        safe=False,
        json_dumps_params={'ensure_ascii': False}
    )


@require_http_methods(["POST"])
def send_message(request, user_id):
    form = MessageForm(request.POST, user_id=user_id)
    # print(request.POST.get('content'))
    if form.is_valid():
        message = form.save()
        return JsonResponse('OK', safe=False)
        # return HttpResponse(list(lat_mes))
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@require_http_methods(["POST"])
def read_mess(request, user_id, chat_id):
    member_of_chat = get_object_or_404(Member, chat_id=chat_id, user_id=user_id)
    message = Message.objects.filter(chat_id=chat_id).filter(user_id=user_id).latest('added_at')
    member_of_chat.new_messages = False
    member_of_chat.last_read_message = message
    member_of_chat.save()
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

    returnedTrue()

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


@require_http_methods(["POST"])
def attachment_save(request):
    form = AttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 200})
    else:
        print(form.errors)
        return JsonResponse({'errors': form.errors}, status=400)


@require_http_methods(["GET"])
def get_attachment(request, attachment_id, user_id):
    try:
        attach = Attachment.objects.get(id=attachment_id)
        member = Member.objects.get(user_id=user_id, chat_id=attach.chat.id)
    except Attachment.DoesNotExist:
        return JsonResponse('No such doc', safe=False)
    except Member.DoesNotExist:
        return JsonResponse('Not Allowed', safe=False)

    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'track_vaganov',
            'Key': attach.file.name,
        },
        ExpiresIn=3600)
    # print(type(url))
    return JsonResponse(url, safe=False)


def returnedTrue():
    return True


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = ChatSerializer

    def get_serializer_class(self):
        if self.action == 'get_list_of_chats':
            return MemberSerializer
        if self.action == 'get_particular_chat':
            return ChatSerializer
        if self.action == 'create_chat':
            return NewChatSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False, url_path='user/(?P<user_id>[^/.]+)')
    def get_list_of_chats(self, request, user_id=None):
        queryset = self.get_queryset()
        all_membership_in_chats = queryset.filter(user_id=user_id)

        if all_membership_in_chats.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(all_membership_in_chats, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response({'chats': 'Not Found'}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='user/(?P<user_id>[^/.]+)/chat/(?P<chat_id>[^/.]+)')
    def get_particular_chat(self, request, user_id=None, chat_id=None):
        try:
            queryset = self.get_queryset()
            member_in_chat = queryset.get(user_id=user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            return Response({'error': 'Not such Member'}, status.HTTP_404_NOT_FOUND)
        except Member.MultipleObjectsReturned:
            return Response({'error': 'To much Members'}, status.HTTP_400_BAD_REQUEST)

        chat = member_in_chat.chat
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(chat, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='(?P<user_id>[^/.]+)/newchat')
    def create_chat(self, request, user_id=None):
        serializer_class = self.get_serializer_class()
        form = serializer_class(data=request.POST, context={'user_id': user_id})
        if form.is_valid():
            chat = form.save()
            member = Member.objects.create(user_id=user_id, chat=chat)
            return Response({'chat_id': chat.id}, status.HTTP_200_OK)
        return Response({'error': form.errors}, status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer

    def get_serializer_class(self):
        if self.action == 'message_list':
            return MessageListSerializer
        if self.action == 'send_message':
            return NewMessageSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False, url_path='(?P<user_id>[^/.]+)')
    def message_list(self, request, user_id=None):
        chat_id = request.GET.get('chat_id', None)
        try:
            member_of_chat = Member.objects.get(chat_id=chat_id, user_id=user_id)
        except Member.DoesNotExist:
            return Response({'error': 'Non valid info'}, status.HTTP_400_BAD_REQUEST)

        all_messages = self.get_queryset().filter(chat_id=chat_id).order_by('added_at')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(all_messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='send_message/(?P<user_id>[^/.]+)')
    def send_message(self, request, user_id=None):
        chat_id = request.POST.get('chat_id', None)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.POST, context={'user_id': user_id, 'chat_id': chat_id})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Message successfully saved'}, status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='mark/user/(?P<user_id>[^/.]+)/chat/(?P<chat_id>[^/.]+)')
    def mark_message(self, request, user_id=None, chat_id=None):
        try:
            member_of_chat = Member.objects.get(chat_id=chat_id, user_id=user_id)
        except Member.DoesNotExist:
            return Response({'error': 'Not such member.'}, status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        message = queryset.filter(chat_id=chat_id).filter(user_id=user_id).latest('added_at')
        member_of_chat.new_messages = False
        member_of_chat.last_read_message = message
        member_of_chat.save()
        return Response({'status': 'successfully marked'}, status.HTTP_200_OK)



