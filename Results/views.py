from rest_framework.generics import GenericAPIView
from Results.serializers import ResultSerializer,InstitutionResultSerializer
from rest_framework.response import Response
from rest_framework import status
from Institutions.models  import Institution
from Exams.models import Exam
from InstitutionClasses.models import InstitutionClass
from Results.models import Result
from datetime import datetime
from collections import defaultdict
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
class InstitutionResultView(GenericAPIView):
    serializer_class = InstitutionResultSerializer

    def post(self,request):
        institution_name = request.data.get('institution_name')
        exam_name = request.data.get('exam_name')
        class_code = request.data.get('class_code')
        term = request.data.get('term')
        year = request.data.get('year')
        if not institution_name:
            return Response({
                "status":"error",
                "message":"the institution name is required"
                },status=status.HTTP_400_BAD_REQUEST)
        #get the institution here
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            return Response({
                "status":"error",
                "message":"the institution does not exist"
                },status=status.HTTP_400_BAD_REQUEST)
        try:
            exam = Exam.objects.get(institution=institution,exam_name=exam_name)
        except Exam.DoesNotExist:
            return Response({
                "status": "error",
                "message": {
                "exam_name": ["the exam does not exist"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            form = InstitutionClass.objects.get(institution=institution,class_code=class_code)
        except  InstitutionClass.DoesNotExist:
            return Response({
                "status":"error",
                "message":{
                    "class_code":["the class does not exist in the institution"]
                    }
                },status=status.HTTP_400_BAD_REQUEST)
        results = Result.objects.filter(
            institution=institution,
            exam=exam,
            term=term,
            year=year if year else datetime.now().year,
            )
        grouped_results = defaultdict(list)
        sorted_results = results.select_related('subject', 'student').order_by(
            'student__id', 'subject__subject_code'
        )
        for result in sorted_results:
            grouped_results[result.student].append(result)

        response_data = []
        for student, student_results in grouped_results.items():
            serialized_results = InstitutionResultSerializer(student_results, many=True).data
            response_data.append({
                "student": str(student),
                "adm": str(student.adm_no),
                "results": serialized_results
            })

        return Response({
            "status":"success",
            "message":"successfully fetched  the data",
            "data":response_data
            }, status=status.HTTP_200_OK)