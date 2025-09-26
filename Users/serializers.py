from rest_framework import serializers
from Users.models import User
from Institutions.models import Institution

class UserSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)  # we post this

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'password', 'institution_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_institution_name(self, value):
        try:
            institution = Institution.objects.get(name=value)
        except Institution.DoesNotExist:
            raise serializers.ValidationError("Institution with this name does not exist.")
        return institution  # replace string with actual object

    def create(self, validated_data):
        institution = validated_data.pop('institution_name')  # now it's the Institution object
        user = User.objects.create_user(
            institution=institution,
            **validated_data
        )
        return user