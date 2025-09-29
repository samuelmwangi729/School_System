from InstitutionClasses.serializers import ClassesSerializer
from rest_framework import status, response, serializers
from InstitutionClasses.models import InstitutionClass as Classes
from rest_framework.generics import GenericAPIView

class InstitutionClassView(GenericAPIView):

    serializer_class = ClassesSerializer

    def get(self,request):
        queryset = Classes.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response({
            "status":"success",
            "message":"successfuly fetched the classes",
            "data":serializer.data
            },status=status.HTTP_200_OK)

    #receive the post data 
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"class successfully created",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)
        return response.Response({
            "status":"error",
            "message":serializer.errors,
            },status=status.HTTP_201_CREATED)