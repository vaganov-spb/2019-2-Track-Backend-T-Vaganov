from django.contrib import admin
from chats.models import Chat, Message, Attachment

class ChatAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class AttachmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment, AttachmentAdmin)