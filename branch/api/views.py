from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from branch.api.serializers import BranchSerializers,Branch
from survey import models as surveys
class ListBranch(APIView):
    def get(self, request):
        branches = Branch.objects.all()
        ListBranch=[]
        for branch in branches :
            sql='SELECT 1 id,AVG(answer1) answer1, AVG(answer2) answer2, AVG(answer3) answer3 ,count(answer1) number from survey_survey where branch_id=%s and status=2 GROUP BY branch_id'
            promedio=0
            for survey in surveys.Survey.objects.raw(sql,[branch.id]):
                promedio=round((survey.answer1+survey.answer2+survey.answer3)/3,2)                
            ListBranch.append({"id":branch.id,"name_branch":branch.name_branch,"stars":promedio})
        return Response(ListBranch)

class CreateBranch(APIView):
    def post(self,request):
        serializer = BranchSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)