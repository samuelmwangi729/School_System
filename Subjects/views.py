from rest_framework.generics import GenericAPIView
from Subjects.serializers import SubjectSerializer
from Subjects.models import Subject
from rest_framework import response, status


class subjectsView(GenericAPIView):
    serializer_class = SubjectSerializer

    def get(self,request):
        queryset = Subject.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response({
            "status":"success",
            "message":"successfully fetched",
            "data":serializer.data
            },status=status.HTTP_200_OK)
    def post(self,request):
        data = request.data
        #serialize the data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"successfully added the subject",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)
        return response.Response({
            "status":"error",
            "message":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)