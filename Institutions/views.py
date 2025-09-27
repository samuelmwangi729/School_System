from .serializers import institutionSerializer
from rest_framework.generics import ListAPIView
from rest_framework import response,status
class InstitutionView(ListAPIView):
    serializer_class = institutionSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if(serializer.is_valid()):
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        return response.Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)