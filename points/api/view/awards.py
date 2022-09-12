from points.api.views import *

class AwardsList(APIView):
    def get(self,request):
        try:
            awards=models.Awards.objects.all()
            serializer=serializable.AwardsSerializable(awards,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AwardsCreate(APIView):
    def post(self,request):
        try:
            serializer=serializable.AwardsSerializable(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("ok",status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.text,status=status.HTTP_500_INTERNAL_SERVER_ERROR)