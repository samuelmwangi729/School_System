from rest_framework import serializers
from Users.models import User
from Institutions.models import Institution
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from Institutions.models import Institution
from InstitutionClasses.models import InstitutionClass as Classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

class JwtTokenSerializerPair(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user.user_class)
        #added custom fields to the jwt  token here
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['institution'] ="null" if user.institution is None else user.institution.name
        token['role'] = user.role
        token['user_class'] = "null" if user.user_class is None else user.user_class.class_name

        return token
class UpdateUserSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    class_code = serializers.CharField(write_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    user_class = serializers.StringRelatedField()
    class Meta:
        model=User
        fields=['class_code','institution_name','username','first_name','last_name','role','user_class']
    def validate(self,attrs):
        username = attrs.get('username')
        institution_name = attrs.get('institution_name')
        class_code = attrs.get('class_code')
        try:
            #check if the user exists in an institution]
            #start by validating the institution
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                "institution":"institution does not exist"
                })
        #get the username here
        try:
            user = User.objects.get(username=username)
            print(user.role)
            # if user.role != 'student':
            #     raise serializers.ValidationError({"user":"user must be a student"})
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "user":"user does not exist"
                })
        try:
            form = Classes.objects.get(institution=institution,class_code=class_code)
        except Classes.DoesNotExist:
            raise serializers.ValidationError({
                "class":"the class does not exist"
                })
        attrs['user'] = user
        attrs['user_class'] = form
        return attrs
        #then the create method, you get the user and update the classes here
    def create(self,validated_data):
        validated_data.pop('class_code')
        validated_data.pop('institution_name')
        user = User.objects.get(username=validated_data['username'])
        user.user_class = validated_data['user_class']
        user.save()
        return user