from rest_framework import serializers
from Users.models import User
from Institutions.models import Institution
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from Institutions.models import Institution

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)  # input only
    institution = serializers.StringRelatedField(read_only=True)  # output only

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'institution_name', 'institution', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},  # Optional: auto-generate
        }

    def validate(self, attrs):
        institution_name = attrs.get('institution_name')

        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                'institution_name': "Institution with this name does not exist."
            })

        attrs['institution'] = institution  # Add the institution object to the validated data
        return attrs

    def create(self, validated_data):
        validated_data.pop('institution_name')  # No longer needed
        password = validated_data.pop('password')
        
        # Optionally generate username if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    institution = serializers.StringRelatedField(read_only=True)
    password = serializers.CharField(
        max_length=128,min_length=6,write_only=True
        )

    class Meta:
        model = User
        fields = ('email','username','role','institution','password','token')
        read_only_fields=['token']
    def get_token(self, obj):
        return obj.token