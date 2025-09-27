from rest_framework import serializers
from Institutions.models import Institution

class institutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields=["name","subcounty","county","category","institutionType","studentGender","status"]

    #create institution here 
    def validate_name(self, value):
        if Institution.objects.filter(name=value).exists():
            raise serializers.ValidationError("Institution with this name already exists.")
        return value
    
    def create(self,validated_data):
        institution = Institution.objects.create(**validated_data)
        return institution