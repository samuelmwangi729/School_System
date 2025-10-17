from rest_framework.serializers import ValidationError
from rest_framework import serializers
from InstitutionClasses.models import InstitutionClass as Classes
from Users.models import User
from Institutions.models import Institution

class ClassesSerializer(serializers.ModelSerializer):
    #check the inputs here 
    #if its keyed in, it should be writer_only, else erad_only
    institution_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    institution = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Classes
        fields=['class_code','class_name','institution','institution_name',
                'class_status','username']
    #declare the validate method 
    '''
    1. check if the institution exists
    2. check if the user exists
    3. check if the class code exists
    4. class name exists here
    '''
    def validate(self,attrs):
        #get the params 
        username = attrs.get('username')
        institution_name = attrs.get('institution_name')
        class_code = attrs.get('class_code')
        class_name = attrs.get('class_name')

        try:
            institution  = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                "institution_name":"institution does not exist"
                })
        try:
            user = User.objects.get(username=username)
            if user.role not in ['admin', 'super_admin']:
                raise serializers.ValidationError({"user":"you dont have the permission to perform this action"})
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "username":"user does not exist"
                })
        if Classes.objects.filter(class_name=class_name,institution=institution).exists():
            raise serializers.ValidationError({
                "class_name":"the class with the same name exists!"
                })
        if Classes.objects.filter(class_code=class_code,institution=institution).exists():
            raise serializers.ValidationError({
                "class_code":"the class with the same code exists!"
                })
        attrs['institution']  = institution
        
        return attrs
    def create(self,validated_data):
        #pop the writeonly fields here 
        validated_data.pop('username')
        validated_data.pop('institution_name')
        student_class = Classes.objects.create(**validated_data)
        
        return student_class