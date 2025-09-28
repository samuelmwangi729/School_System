from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate,login

from Users.serializers import UserSerializer,LoginSerializer
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
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        user = authenticate(username=email,password=password)
        #load the roles here for the user to be returned
        if user is not None:
            serializer = self.serializer_class(user)
            return Response({
                "status":"success",
                "user":serializer.data
                },status = status.HTTP_200_OK)
        return Response({
            "status":"error",
            "message":"invalid credentials used"
            },status = status.HTTP_401_UNAUTHORIZED)