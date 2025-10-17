from rest_framework.generics import GenericAPIView
from Exams.serializers import ExaminationSerializers
from Exams.models import Exam
from rest_framework import response,status
from rest_framework.response import Response
from Institutions.models  import Institution
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class ExaminationView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExaminationSerializers
    def get(self,request):
        queryset = Exam.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response({
            "status":"success",
            "message":"examinations successfully fetched",
            "data":serializer.data
            },status=status.HTTP_200_OK)

    def post(self,request):
        # institution_name = request.data.get('institution',None)
        # username = request.data.get('username',None)
        # title = request.data.get('title',None)
        # term = request.data.get('term',None)
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"created the exam",
                "data":serializer.data
                },status=status.HTTP_200_OK)
        return response.Response({
            "status":"error",
            "message":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,exam_name=None):
        institution_name = request.data.get("institution_name")
        if not institution_name:
            return Response({
                "status": "error",
                "message": "institution_name is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Institution does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            exam = Exam.objects.get(institution=institution, exam_name=exam_name)
        except Exam.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Exam does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)