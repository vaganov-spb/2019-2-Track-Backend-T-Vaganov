from rest_framework import serializers
from chats.models import Chat, Message, Attachment
from users.models import Member, User


class MemberSerializer(serializers.ModelSerializer):
    last_read_message_content = serializers.ReadOnlyField(source='last_read_message.content')
    last_read_message_added_at = serializers.ReadOnlyField(source='last_read_message.added_at')
    chat_topic = serializers.ReadOnlyField(source='chat.topic')
    user_avatar = serializers.ImageField(source='user.avatar', allow_empty_file=True)

    class Meta:
        model = Member
        fields = ('chat_id',
                  'new_messages',
                  'chat_topic',
                  'user_avatar',
                  'last_read_message_content',
                  'last_read_message_added_at')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'topic', 'last_message', 'is_group_chat']


class NewChatSerializer(serializers.ModelSerializer):
    def validate_topic(self, value):
        if not any(c.isalpha() for c in value):
            raise serializers.ValidationError("Not Correct Topic.")
        return value

    def validate(self, data):
        user_id = self.context.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Not Such User.")
        return data

    class Meta:
        model = Chat
        fields = ['topic']


class MessageListSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Message
        fields = ['id', 'content', 'added_at', 'user_username']


class NewMessageSerializer(serializers.ModelSerializer):
    def validate(self, data):
        chat_id = self.context.get('chat_id')
        user_id = self.context.get('user_id')
        try:
            member = Member.objects.get(user_id=user_id, chat_id=chat_id)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Not Such User In That Chat.")
        return data

    def create(self, validated_data):
        chat_id = self.context.get('chat_id')
        user_id = self.context.get('user_id')
        message = Message.objects.create(user_id=user_id, chat_id=chat_id, content=validated_data['content'])
        return message

    class Meta:
        model = Message
        fields = ['content', 'chat_id']

