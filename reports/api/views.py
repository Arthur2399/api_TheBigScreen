import calendar
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from points import models as points_models
from survey import models as survey_models
from reports.api import serializers
class report_sale(APIView):
    def post(self,request):
        serialize=serializers.type(data=request.data)
        if serialize.is_valid():
            final={}
            if serialize.validated_data['type']==1 or serialize.validated_data['type']=="month":
                sql="""
                select 1 id, count(*), date_part('month', points_ticket.date) as "month" from points_ticket GROUP BY date_part('month', points_ticket.date) order by date_part('month', points_ticket.date) desc limit 6
                """
                result=[]
                for row in points_models.Ticket.objects.raw(sql):
                    row_data={
                        "month_number":int(row.month),
                        "month_name":calendar.month_name[int(row.month)],
                        "count":row.count
                    }
                    result.append(row_data)
                final={
                    "name":"Ventas por mes",
                    "data":result
                }
            elif serialize.validated_data['type']==2 or serialize.validated_data['type']=="day":
                sql="""
                select 1 id, count(*), date_part('day', points_ticket.date) as "day" from points_ticket GROUP BY date_part('day', points_ticket.date) order by date_part('day', points_ticket.date) desc limit 6
                """
                result=[]
                for row in points_models.Ticket.objects.raw(sql):
                    row_data={
                        "day_number":int(row.day),
                        "count":row.count
                    }
                    result.append(row_data)
                final={
                    "name":"Ventas por día",
                    "data":result
                    }
            print(final)
            return Response(final,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class report_survey(APIView):
    def post(self,request):
        serialize=serializers.report_survey(data=request.data)
        if serialize.is_valid():
            finals={}
            if serialize.validated_data["branch_id"]==0:
                # sql="""
                # select 1 id,count(*), branch_id , status from survey_survey GROUP BY status,branch_id;
                # """
                # result=[]
                # for row in survey_models.Survey.objects.raw(sql):
                #     final={
                #         "branch":row.branch.name_branch,
                #         "status":row.status,
                #         "count":row.count
                #     }
                #     result.append(final)
                sql="""
                select 1 id,count(*) , status from survey_survey GROUP BY status;
                """
                result=[]
                for row in survey_models.Survey.objects.raw(sql):
                    final={
                        "status":row.status,
                        "count":row.count
                    }
                    result.append(final)    
                total=survey_models.Survey.objects.count()
                finals={
                    "total":total,
                    "result":result
                }
            else:
                sql="select 1 id, count(*) , status from survey_survey where branch_id= %s GROUP BY status;"
                result=[]
                for row in survey_models.Survey.objects.raw(sql,[serialize.validated_data["branch_id"]]):
                    final={
                        "status":row.status,
                        "count":row.count
                    }
                    result.append(final)
                total=survey_models.Survey.objects.filter(branch_id=serialize.validated_data["branch_id"]).count()
                finals={
                    "total":total,
                    "result":result
                    }
            return Response(finals,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class reportGlobal(APIView):
    def get(self,request):
        sql="""
        SELECT 1 id , "sum"(answer1) as a1, "sum"(answer2) a2, "sum"(answer3) as a3, "sum"(answer4) as a4 from survey_survey where status = 2;
        """
        data=[0,0,0,0]
        for x in survey_models.Survey.objects.raw(sql):
            data=[x.a1,x.a2,x.a3,x.a4]
        return Response(data,status.HTTP_200_OK)

