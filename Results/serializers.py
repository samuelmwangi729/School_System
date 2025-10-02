from rest_framework import serializers
from Results.models import Result
from Institutions.models import Institution
from Exams.models import EXAMTERMS, Exam
from Users.models import User
from Subjects.models import Subject

class ResultSerializer(serializers.ModelSerializer):
    #for read only from the database
    institution = serializers.StringRelatedField(read_only=True)
    exam = serializers.StringRelatedField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    grade = serializers.StringRelatedField(read_only=True)
    form = serializers.StringRelatedField(read_only=True)

    #input that will not be required and will have 
    #to be popped later in the update and create method
    institution_name = serializers.CharField(write_only=True)
    exam_name = serializers.CharField(write_only=True)
    teacher_name = serializers.CharField(write_only=True)
    student_name = serializers.CharField(write_only=True)
    subject_code = serializers.CharField(write_only=True)
    class_code = serializers.CharField(write_only=True)
    #the grade will be checked later on the subject

    class Meta:
        model = Result
        fields=['institution','exam','term','teacher','student',
                'subject','mark','grade','institution_name','exam_name','teacher_name',
                'student_name','subject_code','class_code','form'
                ]

        #validate the data to be posted 
        def validate(self,attrs):
            institution_name =attrs.get('institution_name')
            exam_name =attrs.get('exam_name')
            teacher_name =attrs.get('teacher_name')
            student_name =attrs.get('student_name')
            subject_code =attrs.get('subject_code')
            print(attrs)
            return attrs