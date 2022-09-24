from datetime import datetime
from gzip import READ
from movies.api.views import *
from django.utils import timezone
from survey import models as survey

def set_Schedule(movies):
    for x in models.Branch.objects.all():
       schedule=models.Schedule()
       schedule.movies_schedule_id=movies
       schedule.branch_schedule_id=x.id
       schedule.save()
    return True
class Movies (APIView):
    def get(self,request):
        try:
            date=timezone.now().strftime("%Y-%m-%d")
            movie=models.movies.objects.filter(departure_date_movie__gte=date)
            cont=0
            movies=[]
            for a in movie:
                print(a.premiere_date_movie)
                movies.append(a)
                #print(movies[cont])
                if datetime.strftime(a.premiere_date_movie,"%Y-%m-%d")>date:
                    movies[cont].premiere=True
                else:
                    movies[cont].premiere=False
                print(movies[cont].premiere)
                cont+=1
            movies = serializable.moviesSerializable(movies, many=True)
            return Response(movies.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        print(request.data)
        movie=serializable.moviesSerializable(data=request.data)
        if movie.is_valid():
            movie.save()
            set_Schedule(movie.data["id"])
            return Response(movie.data,status=status.HTTP_201_CREATED)
        return Response(movie.errors,status=status.HTTP_400_BAD_REQUEST)
#        except Exception as e:
#            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieUpdate (APIView):
    def get(self, request, id):
        movie = serializable.models.movies.objects.get(pk=id)
        serializer = serializable.moviesSerializable(instance=movie)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, id):
        movie = serializable.models.movies.objects.get(pk=id)
        serializer = serializable.moviesSerializable(instance=movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            



class NextPremiere (APIView):
    def get(self,request):
        try:
            date=timezone.now().strftime("%Y-%m-%d")
            movie=models.movies.objects.filter(departure_date_movie__gte=date)
            #print(movie)
            cont=0
            movies=[]
            for a in movie:
                #print(a.premiere_date_movie)
                movies.append(a)
                #print(movies)
                #print(movies[cont])
                print(datetime.strftime(a.premiere_date_movie,"%Y-%m-%d")>date)
                print(cont)
                if datetime.strftime(a.premiere_date_movie,"%Y-%m-%d")>date:
                    print('pass')
                    movies[cont].premiere=True
                    serializer=serializable.moviesSerializable(movies[cont])
                    return Response(serializer.data,status=status.HTTP_200_OK)
                cont+=1
            print("None")
            data={
                "name_movie":"No hay estreno",
                "photo_movie":"/media/movies/NoEstreno.jpeg",
                "category_movie":[],
                "actor_movie":[],
                "premiere_date_movie":""
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class bestMovie(APIView):
    def get(self,request):
        try:
            raw='SELECT 1 id, movies_id, AVG(answer4) "Estrella" ,count(movies_id) "number" from survey_survey where status=2 GROUP BY movies_id ORDER BY  "Estrella" Desc,"number" desc limit 1'
            movie={}
            for a in survey.Survey.objects.raw(raw):
                movie={
                    "name_movie":a.movies.name_movie,
                    "photo_movie":a.movies.photo_movie.url,
                    "stars":round(a.Estrella,2),
                    "numbers":a.number,
                }
            serializer=serializable.BestMovie(movie)
            return Response(movie,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class bestMovie5(APIView):
    def get(self,request):
        try:
            raw='SELECT 1 id, movies_id, AVG(answer4) "Estrella" ,count(movies_id) "number" from survey_survey where status=2 GROUP BY movies_id ORDER BY  "Estrella" Desc,"number" desc limit 5'
            movies=[]
            for a in survey.Survey.objects.raw(raw):
                movie=[{
                    "name_movie":a.movies.name_movie,
                    "photo_movie":a.movies.photo_movie.url,
                    "stars":round(a.Estrella,2),
                    "numbers":a.number,
                }]
                for g in movie:
                    movies=movies+[g]
            return Response(movies,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
