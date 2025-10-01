from rest_framework import serializers
from Subjects.models import Subject
from Institutions.models import Institution
from Users.models import User

class SubjectSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    institution = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subject
        fields = [
            'institution_name', 'subject_code', 'subject_name',
            'created_by', 'username', 'institution', 'status'
        ]

    def validate(self, attrs):
        # Detect if this is an update
        is_update = self.instance is not None

        # Get fields or fallback to instance if updating
        institution_name = attrs.get('institution_name') or (self.instance.institution.name if is_update else None)
        username = attrs.get('username') or (self.instance.created_by.username if is_update else None)
        subject_code = attrs.get('subject_code') or (self.instance.subject_code if is_update else None)
        subject_name = attrs.get('subject_name') or (self.instance.subject_name if is_update else None)

        # --- Institution check ---
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            raise serializers.ValidationError({
                "institution_name": "Institution with this name does not exist."
            })

        # --- User check ---
        try:
            user = User.objects.get(username=username)
            if user.role not in ['admin', 'super_admin']:
                raise serializers.ValidationError({
                    "username": "You must be an admin to perform this action."
                })
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "username": "User with this username does not exist."
            })

        # --- Duplicate checks (exclude self if updating) ---
        duplicate_qs = Subject.objects.filter(
            subject_code=subject_code,
            subject_name=subject_name,
            institution=institution
        )
        if is_update:
            duplicate_qs = duplicate_qs.exclude(pk=self.instance.pk)
        if duplicate_qs.exists():
            raise serializers.ValidationError({
                "subject_name": "A subject with this code and name already exists for this institution."
            })

        # Optional: separate checks if needed
        duplicate_name_qs = Subject.objects.filter(
            subject_name=subject_name,
            institution=institution
        )
        if is_update:
            duplicate_name_qs = duplicate_name_qs.exclude(pk=self.instance.pk)
        if duplicate_name_qs.exists():
            raise serializers.ValidationError({
                "subject_name": "A subject with this name already exists for this institution."
            })

        duplicate_code_qs = Subject.objects.filter(
            subject_code=subject_code,
            institution=institution
        )
        if is_update:
            duplicate_code_qs = duplicate_code_qs.exclude(pk=self.instance.pk)
        if duplicate_code_qs.exists():
            raise serializers.ValidationError({
                "subject_code": "A subject with this code already exists for this institution."
            })

        # --- Attach related objects to attrs ---
        attrs['created_by'] = user
        attrs['institution'] = institution

        return attrs

    def create(self, validated_data):
        validated_data.pop('institution_name')
        validated_data.pop('username')
        return Subject.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('institution_name', None)
        validated_data.pop('username', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
