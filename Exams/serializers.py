from django.forms import fields
from rest_framework import serializers
from Exams.models import Exam, ExaminationStatus
from Institutions.models import Institution
from Users.models import User

class ExaminationSerializers(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    exam_status = serializers.CharField(default="active")
    username = serializers.CharField(write_only=True)
    institution = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Exam
        fields = [
            'username', 'institution_name', 'exam_name', 'exam_term',
            'created_by', 'exam_status', 'exam_year', 'institution'
        ]

    def validate(self, attrs):
        institution_name = attrs.get('institution_name')
        username = attrs.get('username')
        exam_name = attrs.get('exam_name')

        # Validate Institution
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

        # Prevent duplicate exams (excluding self on update)
        existing_exam = Exam.objects.filter(exam_name=exam_name, institution=institution)
        if self.instance:
            existing_exam = existing_exam.exclude(pk=self.instance.pk)
        if existing_exam.exists():
            raise serializers.ValidationError({
                "exam_name": "An exam with this name already exists for the specified institution."
            })

        # Attach for use in create/update
        attrs['created_by'] = user
        attrs['institution'] = institution

        return attrs

    def create(self, validated_data):
        validated_data.pop('institution_name')
        validated_data.pop('username')
        return Exam.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('institution_name', None)
        validated_data.pop('username', None)
        exam_status=validated_data.get('exam_status')
        valid_choices = [choice[0] for choice in ExaminationStatus.choices]
        if exam_status and exam_status not in valid_choices:
            raise serializers.ValidationError({
                "exam_status": "invalid status sent"
            })
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
