from rest_framework.generics import GenericAPIView
from django.template.context_processors import request
from Exams.serializers import ExaminationSerializers
from Exams.models import Exam
from rest_framework import response,status
from Institutions.models  import Institution
class ExaminationView(GenericAPIView):
    #get the examinations here 
    serializer_class = ExaminationSerializers
    def get(self,request):
        queryset = Exam.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response({
            "status":"success",
            "message":"examinations successfully fetched",
            "data":serializer.data
            },status=status.HTTP_200_OK)

    def post(self,request):
        # institution_name = request.data.get('institution',None)
        # username = request.data.get('username',None)
        # title = request.data.get('title',None)
        # term = request.data.get('term',None)
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"created the exam",
                "data":serializer.data
                },status=status.HTTP_200_OK)
        return response.Response({
            "status":"error",
            "message":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,exam_name=None):
        #load the examination here
        institution_name = request.data.get("institution_name")
        institution = Institution.objects.get(name=institution_name)
        try:
            exam = Exam.objects.get(institution=institution,exam_name=exam_name)
        except Exam.DoesNotExist:
            return response.Response({
                "status":"error",
                "message":"the exam does not exist"
                })
        serializer = self.serializer_class(exam,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({
                "status":"success",
                "message":serializer.data
                })
        return response.Response({
                "status":"error",
                "message":serializer.errors
                })
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance