from rest_framework.generics import GenericAPIView
from Teachers.models import Teacher
from Teachers.serializers import TeacherSerializer
from rest_framework import status
from rest_framework.response import Response
class TeacherGenericView(GenericAPIView):
    serializer_class = TeacherSerializer

    def get(self,request):
        queryset = Teacher.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response({
            "status":"success",
            "message":"teachers fetched",
            "data":serializer.data
            },status=status.HTTP_200_OK)
    def post(self,request):
        data = request.data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":"success",
                "message":"teacher successfully added",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)
        return Response({
            "status":"error",
            "message":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)