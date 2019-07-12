from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^library/', include('template_library.urls')),
    url(r'^user/', include('openwisp_users.api.urls'))
]
