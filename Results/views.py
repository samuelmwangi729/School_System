from rest_framework.generics import GenericAPIView
from Results.serializers import ResultSerializer
from rest_framework.response import Response
from rest_framework import status

class ResultsApiView(GenericAPIView):
    serializer_class =ResultSerializer
    def get(self,request):
        pass
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":"success",
                "message":"successfully added the results",
                "data":serializer.data
                })
        return Response({
                "status":"error",
                "message":serializer.errors
                })
    def put(self,request):
        pass