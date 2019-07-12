from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.shortcuts import redirect
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CustomConfirmEmailView(ConfirmEmailView):
    """
    Override default register view to
    redirect users to create organizations
    after signup
    """

    def post(self, *args, **kwargs):
        redirect_url = 'list_orgs'
        super(CustomConfirmEmailView, self).post(*args, **kwargs)
        return redirect(redirect_url)


confirm_email = CustomConfirmEmailView.as_view()
fb_login = FacebookLogin.as_view()
google_login = GoogleLogin.as_view()
