from .serializers import InstitutionSerializer
from rest_framework.views import APIView
from rest_framework import response,status
from Institutions.models import Institution
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class InstitutionView(APIView):
    serializer_class = InstitutionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if(serializer.is_valid()):
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"institution successfully created",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)
        return response.Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        queryset = Institution.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,institution_name=None):
        #search the institution
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            return response.Response({
                "status":"error",
                "message":"the institution does not exist"
                })
        serializer = self.serializer_class(institution,data =request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"successfully updated the institution"
                })
        return response.Response({
                "status":"error",
                "message":serializer.errors
                })