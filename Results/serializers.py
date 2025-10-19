from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Results.models import Result
from Institutions.models import Institution
from Exams.models import Exam
from Users.models import User
from Subjects.models import Subject
from InstitutionClasses.models import InstitutionClass
from datetime import datetime
class ResultSerializer(serializers.ModelSerializer):
    #for read only from the database
    institution = serializers.StringRelatedField(read_only=True)
    exam = serializers.StringRelatedField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    grade = serializers.StringRelatedField(read_only=True)
    form = serializers.StringRelatedField(read_only=True)
    student = serializers.StringRelatedField(read_only=True)
    mark = serializers.IntegerField(default=0)
    grade = serializers.CharField(default="A")

    #input that will not be required and will have 
    #to be popped later in the update and create method
    institution_name = serializers.CharField(write_only=True)
    exam_name = serializers.CharField(write_only=True)
    teacher_name = serializers.CharField(write_only=True)
    student_admno = serializers.CharField(write_only=True)
    subject_code = serializers.CharField(write_only=True)
    class_code = serializers.CharField(write_only=True)
    #the grade will be checked later on the subject

    class Meta:
        model = Result
        fields=['institution','exam','term','teacher','student',
                'subject','mark','grade','institution_name','exam_name','teacher_name',
                'student_admno','subject_code','class_code','form'
                ]

    #validate the data to be posted 
    def validate(self,attrs):
        institution_name =attrs.get('institution_name')
        exam_name =attrs.get('exam_name')
        teacher_name =attrs.get('teacher_name')
        student_admno =attrs.get('student_admno')
        subject_code =attrs.get('subject_code')
        class_code =attrs.get('class_code')
        term =attrs.get('term')
        
        #check if the institution exists
        #check the marks ranges from 0-99
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({"institution_name":"institution does dot exist"})
        #get the user from the users, whose role is student and adm number is the one sent here
        try:
            student = User.objects.get(institution=institution,adm_no=student_admno,role="student")
        except User.DoesNotExist:
            raise serializers.ValidationError({"student_admno":"the student does not exist"})
        try:
            exam = Exam.objects.get(institution=institution,exam_name=exam_name)
        except Exam.DoesNotExist:
            raise serializers.ValidationError({"exam_name":"the exam does not exist"})
        try:
            teacher = User.objects.get(institution=institution,username=teacher_name)
        except User.DoesNotExist:
            raise serializers.ValidationError({"teacher_name":"the teacher does not exist"})
        try:
            subject = Subject.objects.get(subject_code=subject_code,institution=institution)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject_code":"the subject does not exist"})
        try:
            form = InstitutionClass.objects.get(institution=institution,class_code=class_code)
        except  InstitutionClass.DoesNotExist:
            raise serializers.ValidationError({"class_code":"the class does not exist"})
        #check if the marks of the same exam,same subject,same year,same term,same student has been uploaded
        if Result.objects.filter(
            institution=institution,
            exam=exam,
            term=term,
            subject=subject,
            year=datetime.now().year,
            student=student
            ).exists():
            raise serializers.ValidationError({"student_admno":f"the results for {student.first_name} {student.last_name} has already been posted"})

        attrs['institution'] = institution
        attrs['exam'] = exam
        attrs['form'] = form
        attrs['teacher'] = teacher
        attrs['student'] = student
        attrs['subject']=subject
        return attrs
    
    def create(self,validated_data):
        validated_data.pop("institution_name")
        validated_data.pop("exam_name")
        validated_data.pop("teacher_name")
        validated_data.pop("subject_code")
        validated_data.pop("class_code")
        validated_data.pop("student_admno")
        result = Result.objects.create(**validated_data)
        return result

class InstitutionResultSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    exam_name = serializers.CharField(write_only=True)
    term = serializers.CharField(write_only=True)
    year = serializers.CharField(write_only=True,default=datetime.now().year)
    class_code = serializers.CharField(write_only=True)
    institution = serializers.StringRelatedField(read_only=True)
    form = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    student = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Result
        fields=[
            'institution_name','exam_name','term','class_code','year',
            'institution','form','subject','student','mark','grade'
            ]