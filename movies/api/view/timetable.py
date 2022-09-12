from movies.api.views import models,serializable,Response,status,APIView

class TimetableList(APIView):
    def get(self,request):
        timetable = models.Timetable.objects.all()
        serializer = serializable.TimetableSerializer(timetable, many=True)
        return Response(serializer.data)
class TimetableCreate(APIView):
    def post(self,request):
        serializer = serializable.TimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)