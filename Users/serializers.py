from rest_framework import serializers
from Users.models import User
from Institutions.models import Institution

class UserSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)  # input only
    institution = serializers.StringRelatedField(read_only=True)  # output only

    class Meta:
        model = User
        # Include all fields you want returned (exclude password)
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'institution_name', 'institution'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_institution_name(self, value):
        try:
            institution = Institution.objects.get(name=value)
        except Institution.DoesNotExist:
            raise serializers.ValidationError("Institution with this name does not exist.")
        return institution

    def create(self, validated_data):
        institution = validated_data.pop('institution_name')
        user = User.objects.create(
            institution=institution,
            **validated_data
        )
        return user