from django.contrib import admin
from users.models import User, Member

class UserAdmin(admin.ModelAdmin):
    pass

class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
