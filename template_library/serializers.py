from openwisp_utils.api.serializers import ValidatedModelSerializer

from openwisp_users.models import Organization


class OrganizationSerializer(ValidatedModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationCreateUpdateSerializer(ValidatedModelSerializer):

    class Meta:
        model = Organization
        exclude = ('is_active',)
