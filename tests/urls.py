from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^library/', include('template_library.urls')),
    url(r'^users/', include('openwisp_users.api.urls')),
    url(r'^template/', include('openwisp_controller.config.api.urls'))
]
