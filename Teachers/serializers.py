from rest_framework import serializers
from Institutions.models import Institution
from Subjects.models import Subject
from InstitutionClasses.models import InstitutionClass as Classes
from Teachers.models import Teacher
from Users.models import User

class TeacherSerializer(serializers.ModelSerializer):
    #load the fields input from the frontend
    teacher_name = serializers.CharField(write_only=True) #input the teacher name as the username 
    subject_name = serializers.CharField(write_only=True) 
    class_code = serializers.CharField(write_only=True) 
    institution_name = serializers.CharField(write_only=True) #this checks if the teacher exists in the institution
    teacher = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    form = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Teacher
        fields=['institution_name','teacher_name','subject_name','class_code','teacher','subject','form','status']


    #validate the data sent
    def validate(self,data):
        teacher_name = data.get('teacher_name')
        subject_name = data.get('subject_name')
        institution_name = data.get('institution_name')
        class_code = data.get('class_code')

        try:
            #check if the user exists in an institution]
            #start by validating the institution
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                "institution":"institution does not exist"
                })
        try:
            teacher = User.objects.get(username=teacher_name,institution=institution)
            #you role must be a teacher 
            # if teacher.role !="teacher":
            #     raise serializers.ValidationError({"teacher":"the user is not registered as a teacher"})

        except User.DoesNotExist:
             raise serializers.ValidationError({"teacher":"teacher with the username does not exist in the institution"})
        #check the subject exists in the institution
        try:
            subject = Subject.objects.get(institution=institution,subject_name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject":"subject does not exist"})
        try:
            form = Classes.objects.get(institution=institution,class_code=class_code)
        except Classes.DoesNotExist:
            raise serializers.ValidationError({
                "class":"the class does not exist"
                })
        #check no teacher should be added same class, same subject and same form
        if Teacher.objects.filter(teacher=teacher,subject=subject,form=form).exists():
            raise serializers.ValidationError({
                "teacher":"teacher already added"
                })
        #limit the teacher to teach only two subjects per form
        if Teacher.objects.filter(teacher=teacher,form=form).count()==2:
            raise serializers.ValidationError({
                "teacher":f"Mr {teacher.last_name} can only teach a maximum of 2 subjects in {form.class_name}"
                })
        data['form'] = form
        data['teacher'] = teacher
        data['subject'] = subject

        return data
    def create(self,args):
        args.pop('teacher_name')
        args.pop('institution_name')
        args.pop('subject_name')
        args.pop('class_code')

        teacher = Teacher.objects.create(**args)
        return teacher