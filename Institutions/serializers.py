from rest_framework import serializers
from Institutions.models import Institution

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["name", "subcounty", "county", "category", "institutionType", "studentGender", "status"]

    def validate(self, value):
        # If we're updating and the name hasn't changed, allow it
        if self.instance and self.instance.name == value:
            return value

        # Otherwise, ensure the name is unique across other records
        if Institution.objects.filter(name=value).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError("Institution with this name already exists.")
        return value

    def create(self, validated_data):
        return Institution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance