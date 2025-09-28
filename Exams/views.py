from rest_framework.generics import GenericAPIView
from django.template.context_processors import request
from Exams.serializers import ExaminationSerializers
from Exams.models import Exam
from rest_framework import response,status
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