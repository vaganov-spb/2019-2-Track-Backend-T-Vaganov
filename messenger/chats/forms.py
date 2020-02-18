from django import forms
import uuid
import magic
from chats.models import Chat, Message, Attachment
from users.models import User, Member


class ChatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user_id = kwargs.pop('user_id')
        super(ChatForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(ChatForm, self).clean()
        try:
            user = User.objects.get(id=self._user_id)
        except User.DoesNotExist:
            self.add_error('topic', 'No such user to create chat')
        return self.cleaned_data

    class Meta:
        model = Chat
        fields = ['topic']


class MessageForm(forms.ModelForm):
    chatId = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self._user_id = kwargs.pop('user_id')
        super(MessageForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        try:
            chat_id = cleaned_data['chatId']
            member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            self.add_error('content', 'Cant Find such chat member, check user id or chat id')
        return cleaned_data

    def save(self, *args, **kwargs):
        chat_id = self.cleaned_data['chatId']
        # member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        mes = Message.objects.create(user_id=self._user_id, chat_id=chat_id, content=self.cleaned_data['content'])
        # member.last_read_message = mes
        # member.save()

    class Meta:
       model = Message
       fields = ['content']


class AttachmentForm(forms.ModelForm):
    chat_id = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self._member = None
        super(AttachmentForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data['file']
        if len(file.name) > 100:
            self.add_error('file', 'To long filename')
        return file

    def clean(self):
        cleaned_data = super(AttachmentForm, self).clean()
        chat_id = cleaned_data['chat_id']
        user_id = cleaned_data['user_id']
        try:
            self._member = Member.objects.get(user_id=user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            self.add_error('user_id', 'Can\'t find such chat member, check user_id or chat_id')
        return cleaned_data

    def save(self, *args, **kwargs):
        user = self._member.user
        chat = self._member.chat
        file = self.cleaned_data['file']
        message = Message.objects.create(user=user, chat=chat)
        attachment = Attachment(user=user, chat=chat, message=message)
        attachment.type = magic.from_buffer(file.read(), mime=True)
        attachment.file.save(f'{chat.id}/{uuid.uuid4().hex}', file)
        attachment.name = file.name
        attachment.save()
        return attachment

    class Meta:
        model = Attachment
        fields = ['file']












