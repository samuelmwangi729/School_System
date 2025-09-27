from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from Users.serializers import UserSerializer
class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        data  = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        errors = serializer.errors
        return Response({"errors":errors},status=status.HTTP_400_BAD_REQUEST)