from django import forms
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
        #self.cleaned_data = super(MessageForm, self).clean()
        super(MessageForm, self).clean()
        try:
            chat_id = self.cleaned_data['chatId']
            member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            self.add_error('content', 'Cant Find such chat member, check user id or chat id')
        return self.cleaned_data

    def save(self):
        chat_id = self.cleaned_data['chatId']
        member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        mes = Message.objects.create(user_id=self._user_id, chat_id=chat_id, content=self.cleaned_data['content'])
        member.last_read_message = mes
        member.save()

    class Meta:
       model = Message
       fields = ['content']


class AttachmentForm(forms.Form):
    file = forms.FileField(required=True)
    chat_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self._user_id = kwargs.pop('user_id')
        super(AttachmentForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data['file']
        print(file)
        print(type(file))
        if len(file.url) > 200:
            self.add_error('file', 'To long url of document')
        return file

    def clean(self):
        chat_id = self.cleaned_data['chat_id']
        try:
            member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            self.add_error('content', 'Cant Find such chat member, check user id or chat id')
        return chat_id

    def save(self):
        file = self.cleaned_data['file']
        chat_id = self.cleaned_data['chat_id']
        member = Member.objects.get(user_id=self._user_id, chat_id=chat_id)
        message = Message.objects.create(user_id=self._user_id, chat_id=chat_id)
        attachment = Attachment(user_id=self._user_id, chat_id=chat_id, message=message)
        attachment.type = 'file'
        attachment.url = file.url
        default_storage.save(file.name, file)
        attachment.save()






