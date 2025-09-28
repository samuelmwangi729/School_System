from rest_framework import serializers
from Subjects.models import Subject
from Institutions.models import Institution
from Users.models import User

class SubjectSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    institution = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    #define the meta details here 
    class Meta:
        model = Subject
        fields=['institution_name','subject_code','subject_name','created_by','username','institution','status']
    def validate(self,attrs):
        #get the username and the institution names here
        institution_name = attrs.get('institution_name')
        username = attrs.get('username')
        subject_code = attrs.get('subject_code')
        subject_name = attrs.get('subject_name')
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                "institution_name": "Institution with this name does not exist."
            })

        # Validate User
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "username": "User with this username does not exist."
            })

        # Check for duplicate Exam name for the same institution
        if Subject.objects.filter(subject_code=subject_code,subject_name=subject_name,institution=institution).exists():
            raise serializers.ValidationError({
                "subject_name": "A subject with this code already exists for the specified institution."
            })
        if Subject.objects.filter(subject_name=subject_name,institution=institution).exists():
            raise serializers.ValidationError({
                "subject_name": "A subject with this name already exists for the specified institution."
            })
        attrs['created_by'] = user
        attrs['institution'] = institution

        return attrs


    def create(self,validated_data):
        #create the items here
        validated_data.pop('institution_name')
        validated_data.pop('username')
        subject = Subject.objects.create(**validated_data)
        return subject