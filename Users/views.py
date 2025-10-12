from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Users.models import User
from Users.serializers import LoginSerializer, UpdateUserSerializer, UserSerializer,JwtTokenSerializerPair
from rest_framework_simplejwt.views import TokenObtainPairView,TokenVerifyView
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

@method_decorator(csrf_exempt, name='dispatch')
class UserView(GenericAPIView):
    serializer_class = UpdateUserSerializer
    def get(self,request):
        pass
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            "status":"success",
            "message":"user successfully updated",
            "data":serializer.data
            })
        return Response({
            "status":"error",
            "message":serializer.errors
            })
class JwtTokenObtainView(TokenObtainPairView):
    serializer_class = JwtTokenSerializerPair
    # override the post method here 
    def post(self,request,*args,**kwargs):
        response = super().post(request,*args,**kwargs)
        tokens = response.data
        return Response({"tokens":tokens},status=status.HTTP_200_OK)

class CustomJwtTokenValidator(TokenVerifyView):
    serializer_class = JwtTokenSerializerPair
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"tokens":serializer.data},status=status.HTTP_200_OK)
        return Response({"tokens":"invalid token"},status=status.HTTP_400_BAD_REQUEST)