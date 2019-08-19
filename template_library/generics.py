from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import OrganizationCreateUpdateSerializer, OrganizationSerializer


class BaseOrganizationListCreateAPIView(ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        options = {
            'description': request.POST.get('description', None),
            'name': request.POST.get('name', None),
            'slug': request.POST.get('slug', None),
            'email': request.POST.get('email', None),
            'url': request.POST.get('url', None)
        }
        serializer = OrganizationSerializer(data=options)
        if serializer.is_valid():
            org = serializer.save()
            success = {
                'org_success': 'Organization was successfully created'
            }
            self.org_user_model.objects.create(organization=org, user=request.user)
            return Response(data=success)
        else:
            errors = {
                'org_errors': serializer.errors
            }
            return Response(data=errors, status=400)

    def get_queryset(self):
        orgs = self.org_model.objects.filter(users=self.request.user)
        return orgs


class BaseOrganizationUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationCreateUpdateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_object_or_404(self.org_model, pk=self.kwargs['pk'], users=self.request.user)
