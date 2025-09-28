from django.forms import fields
from rest_framework import serializers
from Exams.models import Exam
from Institutions.models import Institution
from Users.models import User
class ExaminationSerializers(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)  # input only
    username = serializers.CharField(write_only=True) #input username from the frontend 
    institution = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    
    #load the user and the institution
    class Meta:
        model = Exam
        fields=['username','institution_name','exam_name','exam_term','created_by','exam_status','exam_year','institution']

    def validate(self,attrs):
        institution_name = attrs.get('institution_name')
        username = attrs.get('username')
        #raise an error if an exam with the same name is created again
        
        #get the institution name 
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                'status':'error',
                'message': "Institution with this name does not exist."
            })
        #get the user name here 
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "status":"error",
                "message":"user not found"
                })
        attrs['created_by'] = user
        attrs['institution'] = institution
        return attrs

    def create(self,validated_data):
        validated_data.pop('institution_name')
        validated_data.pop('username')
        exam = Exam.objects.create(**validated_data)
        return exam