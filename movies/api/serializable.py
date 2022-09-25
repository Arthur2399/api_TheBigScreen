from rest_framework import serializers
from movies import models
from drf_extra_fields.fields import Base64ImageField
from django.utils import timezone
import datetime
from djcines.settings import DIR,os


class categoriesSerializable(serializers.ModelSerializer):
    class Meta:
        model = models.categories
        fields = "__all__"
class actorsSerializable(serializers.ModelSerializer):
    photo_actor=Base64ImageField(use_url=True,required=True,max_length=None)
    class Meta:
        model = models.actors
        fields = "__all__"

class moviesSerializable(serializers.ModelSerializer):
    category_movie_id = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=models.categories.objects.all()), write_only=True)
    actor_movie_id = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=models.actors.objects.all()), write_only=True) 
    category_movie=serializers.SlugRelatedField(many=True,read_only=True,slug_field='category_name')
    actor_movie=serializers.SlugRelatedField(many=True,read_only=True,slug_field='name_actor')
    premiere=serializers.BooleanField(read_only=True)
    photo_movie=Base64ImageField(use_url=True,required=False,max_length=None)
    class Meta:
        model = models.movies
        fields = "__all__"
    def create(self, validated_data):
        category_movie_id = validated_data.pop('category_movie_id')
        actor_movie_id=validated_data.pop('actor_movie_id')
        movie = models.movies.objects.create(**validated_data)
        for cm in category_movie_id:
            movie.category_movie.add(cm)
        for am in actor_movie_id:
            movie.actor_movie.add(am)
        return movie
class moviesSerializableUpdate(serializers.ModelSerializer):

    category_movie_id = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=models.categories.objects.all()), write_only=True)
    actor_movie_id = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=models.actors.objects.all()), write_only=True) 
    category_movie=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    actor_movie=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    premiere=serializers.BooleanField(read_only=True)
    photo_movie=Base64ImageField(use_url=True,required=False,max_length=None)
    photo_change=serializers.BooleanField(write_only=True,required=False)
    class Meta:
        model = models.movies
        fields = "__all__"
    def update(self, instance, validated_data):
        category_movie_id = validated_data.pop('category_movie_id')
        actor_movie_id=validated_data.pop('actor_movie_id')
        instance.name_movie = validated_data.get('name_movie', instance.name_movie)
        instance.description_movie = validated_data.get('description_movie', instance.description_movie)
        instance.duration_movie = validated_data.get('duration_movie', instance.duration_movie)
        instance.premiere_date_movie = validated_data.get('premiere_date_movie', instance.premiere_date_movie)
        print(instance.photo_movie.url)
        if validated_data.get("photo_change"):
            if os.path.exists(DIR+instance.photo_movie.url):
                os.remove(DIR+instance.photo_movie.url)
            instance.photo_movie=validated_data.get('photo_movie',instance.photo_movie)
        instance.save()
        for x in instance.category_movie:
            x.delete()
        for x in instance.actor_movie:
            x.delete()
        for cm in category_movie_id:
            instance.category_movie.add(cm)
        for am in actor_movie_id:
            instance.actor_movie.add(am)
        return instance
class ScheduleSerializer(serializers.ModelSerializer):
    movies_schedule=serializers.CharField(read_only=True)
    movies_schedule_id=serializers.IntegerField()
    class Meta:
        model = models.Schedule
        fields = "__all__"

class TimetableSerializer(serializers.ModelSerializer):
    #schedule_timetable=serializers.SlugRelatedField(read_only=True,slug_field='movies_schedule_name_movie')
    class Meta:
        model = models.Timetable
        fields = "__all__"
    def validate_day_timetable(self,data):
        if data.strftime("%Y-%m-%d")<timezone.now().strftime("%Y-%m-%d"):
            raise serializers.ValidationError({"Error day_timetable":"La fecha debe ser igual o mayor que hoy"})
        else:
            return data
    def validate(self,data):
        schedule=data.get('schedule_timetable')
        day_timetable=data.get('day_timetable')
        movie=models.movies.objects.filter(id=schedule.movies_schedule_id).values('premiere_date_movie')
        if day_timetable.strftime('%Y-%m-%d')<(movie[0]["premiere_date_movie"]-datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
            raise serializers.ValidationError({"Error day_timetable":"La fecha debe ser igual o mayor que el estreno"})
        else:
            return data
    #def validate_schedule_timetable(self, data):
    #    if movie>data.get('day_timetable'):
    #        raise serializers.ValidationError({"Error day_timetable":"La pelicula no esta disponible en ese dia"})

class BestMovie(serializers.Serializer):
    stars=serializers.FloatField(read_only=True)
    numbers:serializers.IntegerField(read_only=True)
    name_movie=serializers.CharField(read_only=True)
    photo_movie=serializers.CharField(read_only=True)