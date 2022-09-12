from movies.api.views import models,serializable,Response,status,APIView
class Categories(APIView):
    def get(self, request):
        try:
            categories = models.categories.objects.all()
            serializer = serializable.categoriesSerializable(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        try:
            serializer = serializable.categoriesSerializable(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)