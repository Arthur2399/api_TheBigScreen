from movies.api.views import models,serializable,Response,status,APIView
from django.utils import timezone

class ScheduleList(APIView):
    def get(self,request):
            schedule = models.Schedule.objects.all()
            serializer = serializable.ScheduleSerializer(schedule, many=True)
            return Response(serializer.data)

class ScheduleCreate(APIView):
    def post(self,request):
        serializer = serializable.ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Billboard(APIView):
    def get(self,request):
        billboards = []
        date=timezone.now().strftime("%Y-%m-%d")
        time=timezone.now().strftime("%H:%M:%S")
        print(time)
        print(date)
        for i in models.Schedule.objects.raw("select * from movies_schedule inner join movies_movies on movies_schedule.movies_schedule_id= movies_movies.id where %s between movies_movies.premiere_date_movie and movies_movies.departure_date_movie",[date]):
            billboard={}
            cont=0
            timep=[]
            for j in models.Timetable.objects.filter(schedule_timetable_id=i.id,day_timetable=date,hour_timetable__gte=time).order_by("hour_timetable"):
                timep.append({"id":j.id,"time":j.hour_timetable.strftime('%H:%M'),"room":j.room})
                cont+=1
            if len(timep)>0:
                billboard={
                    'id':i.id,
                    'movie_name':i.movies_schedule.name_movie,
                    'movie_photo':i.movies_schedule.photo_movie.url,
                    'branch':i.branch_schedule.name_branch,
                    'movie_date':date,
                    'billboard':timep
                }
                billboards.append(billboard)

        return Response(billboards)

class GetBillboardSchedule(APIView):
    def get(self,request,id):
        billboards = []
        date=timezone.now().strftime("%Y-%m-%d")
        time=timezone.now().strftime("%H:%M:%S")
        print(time)
        print(date)
        for i in models.Schedule.objects.raw("select * from movies_schedule inner join movies_movies on movies_schedule.movies_schedule_id= movies_movies.id where id=%s and %s between movies_movies.premiere_date_movie and movies_movies.departure_date_movie",[id,date]):
            billboard={}
            cont=0
            timep=[]
            for j in models.Timetable.objects.filter(schedule_timetable_id=i.id,day_timetable=date,hour_timetable__gte=time).order_by("hour_timetable"):
                timep.append({"id":j.id,"time":j.hour_timetable.strftime('%H:%M'),"room":j.room})
                cont+=1
            if len(timep)>0:
                billboard={
                    'id':i.id,
                    'movie_name':i.movies_schedule.name_movie,
                    'movie_photo':i.movies_schedule.photo_movie.url,
                    'branch':i.branch_schedule.name_branch,
                    'movie_date':date,
                    'billboard':timep
                }
                billboards.append(billboard)

        return Response(billboards)
            
            