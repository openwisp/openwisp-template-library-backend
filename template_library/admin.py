from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from allauth.socialaccount.admin import SocialAccountAdmin, SocialAppAdmin, SocialTokenAdmin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin

from openwisp_controller.config.models import Device
from openwisp_users.models import Group

# unregister unwanted models
admin.site.unregister(Device)
admin.site.unregister(Group)
# Register wanted and needed module
admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(SocialApp, SocialAppAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(SocialToken, SocialTokenAdmin)
