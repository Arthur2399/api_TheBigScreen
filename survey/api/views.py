
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from survey.api import serializable
from django.utils import timezone


class SurveyTemplateList(APIView):
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    def get(self, request):
        try:
            Survey_template=serializable.models.Survey_template.objects.filter(state=1).first()
            serialize = serializable.SurveyTemplateSerializer(Survey_template)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
            
            serializer=serializable.SurveyTemplateSerializer(data=request.data)
            if serializer.is_valid():
                date=timezone.now().strftime("%Y-%m-%d")
                
                survey_ant=serializable.models.Survey_template.objects.filter(state=1).first()
                
                if survey_ant:
                    print (survey_ant.id)
                    fields={
                        "state":2,
                        "date_final":date
                    }
                    serializable.models.Survey_template.objects.filter(id=survey_ant.id).update(**fields)
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class mobilSurvey(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    def get(self,request):
        try:
            user=request.user.id
            date=timezone.now().strftime("%Y-%m-%d")
            survey=serializable.models.Survey.objects.filter(user_id=user,date=date,status=1)
            serialize=serializable.SurveySerializer(survey,many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class postSurvey(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    def post(self,request,id):
        try:
            surveyValidate=serializable.models.Survey.objects.filter(pk=id,status=1)
            if len(surveyValidate)<1:
                return Response("Esta encuesta ya se ha llenado anteriormente",status=status.HTTP_404_NOT_FOUND)
            survey=serializable.models.Survey.objects.get(pk=id)
            serializer=serializable.surveyAnswer(data=request.data)
            if serializer.is_valid():
                survey.answer1=serializer.data['answer1']
                survey.answer2=serializer.data['answer2']
                survey.answer3=serializer.data['answer3']
                survey.answer4=serializer.data['answer4']
                survey.answer5=serializer.data['answer5']
                survey.status=2
                survey.save()
                
                surveySerializer=serializable.SurveySerializer(survey)
                return Response(surveySerializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
