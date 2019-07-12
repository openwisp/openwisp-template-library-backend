from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^rest-auth/google/$',
        views.google_login,
        name='google_login'),
    url(r'^rest-auth/facebook/$',
        views.fb_login,
        name='fb_login'),
    url(r'^rest-auth/',
        include('rest_auth.urls')),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls')),
    url(r'^accounts/confirm-email/(?P<key>[-:\w]+)/$',
        views.confirm_email,
        name='confirm_email'),
    url(r'^accounts/',
        include('openwisp_users.accounts.urls'))
]
