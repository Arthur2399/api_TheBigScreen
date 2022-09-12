from movies.api.views import APIView,models,serializable,Response,status
class Actors(APIView):
    def get(self,request):
        try:
            actors = models.actors.objects.all()
            serialized_actors = serializable.actorsSerializable(actors, many=True)
            return Response(serialized_actors.data)
        except Exception as e:
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            serialized_actors = serializable.actorsSerializable(data=request.data)
            if serialized_actors.is_valid():
                serialized_actors.save()
                return Response(serialized_actors.data,status=status.HTTP_201_CREATED)
            return Response(serialized_actors.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)