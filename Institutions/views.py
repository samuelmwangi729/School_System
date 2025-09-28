from .serializers import institutionSerializer
from rest_framework.views import APIView
from rest_framework import response,status
from Institutions.models import Institution
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class InstitutionView(APIView):
    serializer_class = institutionSerializer
    # permission_classes=[IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if(serializer.is_valid()):
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        return response.Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        queryset = Institution.objects.all()
        serializer = institutionSerializer(queryset,many=True)
        return response.Response(serializer.data,status=status.HTTP_200_OK)
        