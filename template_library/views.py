from allauth.account.views import ConfirmEmailView as BaseConfirmEmailView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.shortcuts import redirect
from rest_auth.registration.views import SocialLoginView

from openwisp_users.models import Organization, OrganizationUser

from .generics import BaseOrganizationListCreateAPIView, BaseOrganizationUpdateDeleteAPIView


class OrganizationListCreateAPIView(BaseOrganizationListCreateAPIView):
    queryset = Organization.objects.all()
    org_model = Organization
    org_user_model = OrganizationUser


class OrganizationRetrieveUpdateDeleteAPIView(BaseOrganizationUpdateDeleteAPIView):
    queryset = Organization.objects.all()
    org_model = Organization


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ConfirmEmailView(BaseConfirmEmailView):
    """
    Override default email confirmation view to
    redirect users to create organizations
    after signup
    """

    def post(self, *args, **kwargs):
        super(ConfirmEmailView, self).post(*args, **kwargs)
        # redirect users to url with view name list_orgs
        # which handles both creation and listing of organizations
        return redirect('list_orgs')


list_orgs = OrganizationListCreateAPIView.as_view()
org_detail = OrganizationRetrieveUpdateDeleteAPIView.as_view()
confirm_email = ConfirmEmailView.as_view()
fb_login = FacebookLogin.as_view()
google_login = GoogleLogin.as_view()
