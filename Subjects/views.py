from rest_framework.generics import GenericAPIView
from Subjects.serializers import SubjectSerializer
from Subjects.models import Subject
from rest_framework import response, status
from Institutions.models import Institution

class subjectsView(GenericAPIView):
    serializer_class = SubjectSerializer

    def get(self,request):
        queryset = Subject.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return response.Response({
            "status":"success",
            "message":"successfully fetched",
            "data":serializer.data
            },status=status.HTTP_200_OK)
    def post(self,request):
        data = request.data
        #serialize the data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({
                "status":"success",
                "message":"successfully added the subject",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)
        return response.Response({
            "status":"error",
            "message":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,subject_code=None):
        #get the subject here
        institution_name = request.data.get('institution_name')
        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            return response.Response({
                "status":"error",
                "message":"the institution does not exist"
                })
        try:
            subject = Subject.objects.get(subject_code=subject_code,institution=institution)
        except Subject.DoesNotExist:
            return response.Response({
                "status":"error",
                "message":"the subject does not exist"
                })
        serializer = self.serializer_class(instance=subject,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"status":"success","message":"succesfully updated the subject","data":serializer.data})
        return response.Response({"status":"error","message":"could not update the subject","data":serializer.errors})