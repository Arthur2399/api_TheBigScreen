from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from menu.api import serializers
class assignmentList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            menu=[]
            for x in serializers.models.assignment.objects.filter(user=request.user):
                data={
                    "id":x.id,
                    "menu_id":x.menu.id,
                    "menu":x.menu.name,
                    "path":x.menu.path,
                }
                menu.append(data)
            seializer=serializers.assignmentSerializer(menu,many=True)
            return Response(seializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        