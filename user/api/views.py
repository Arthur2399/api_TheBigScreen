from user.api import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User, image
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from djcines.settings import DIR
from utils.crypt import encrypt, decrypt
from utils.QrGenerator import Generator
from points.models import Credits, Ticket
from survey.models import Survey
from rest_framework_simplejwt.authentication import JWTAuthentication
from djcines.settings import DIR, EMAIL_HOST_USER


class usersNew(APIView):
    def post(self, request):
        print(request.FILES)
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            secret = encrypt(str(serializer.data['id']))
            fil = str(serializer.data['id'])+'.png'
            path = "/qr/"
            print(path)
            Generator(secret, path, fil)
            imageupdate = image.objects.filter(
                user=serializer.data['id']).update(qrprofile=path+fil)
            credits = Credits.objects.create(
                number_credits=0, user_id=serializer.data['id'])
            return Response("Registrado correctamente", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeNew(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = serializers.EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializers.SendNew(serializer.data["first_name"]+" "+serializer.data["last_name"],
                serializer.data['password'], serializer.data['email'])
                return Response("Registrado correctamente", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class EmployeeUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request,id):
        employee=serializers.User.objects.get(pk=id)
        print(employee)
        serializer= serializers.EmployeeSerializerUpdate(instance=employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Actualizado correctamente",status=status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class LastEmployee(APIView):
    def get(self, request):
        imagen = image.objects.filter(type="E").order_by("id").last()
        # print(imagen.image.url)
        users = User.objects.filter(id=imagen.user_id).values(
            'id', 'first_name', 'last_name', 'username', 'email', 'date_joined').first()
        # print(users["last_name"])
        datas = {
            'id': users['id'],
            'first_name': users['first_name'],
            'last_name': users['last_name'],
            'username': users['username'],
            'email': users['email'],
            'date_joined': users['date_joined'].strftime("%Y-%m-%d"),
            'image': imagen.image.url,
            'type': imagen.type,
            'rol': imagen.rol.name
        }
        return Response(datas, status=status.HTTP_200_OK)
        # return Response("ok",status=status.HTTP_200_OK)


class EmployeeList(APIView):
    def get(self, request):
        data = []
        datas = {}
        for i in image.objects.filter(type="E"):
            print(i.branch_user_id)
            if i.branch_user == None:
                branch = "Null"
            else:
                branch = i.branch_user.name_branch
            branch = "d"
            users = User.objects.get(id=i.user_id)
            # print(users)
            datas = {
                'id': users.id,
                'first_name': users.first_name,
                'last_name': users.last_name,
                'username': users.username,
                'email': users.email,
                'image': i.image.url,
                'qrprofile': i.qrprofile.url,
                'type': i.type,
                'branch': branch,
                'rol': i.rol.name

            }
            data.append(datas)
        # print(datas)
        # serializer=serializers.UserGetSerializer(data=data,many=True)
        return Response(data, status=status.HTTP_200_OK)


class EmployeeProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        datas = {}
        for i in image.objects.filter(user=request.user.id):
            print(i.user_id)
            users = User.objects.get(id=i.user_id)
            print(users)
            if i.branch_user == None:
                branch = None
            else:
                branch = i.branch_user.name_branch
            datas = {
                'id': users.id,
                'first_name': users.first_name,
                'last_name': users.last_name,
                'username': users.username,
                'email': users.email,
                'image': i.image.url,
                'rol_id': i.rol_id,
                'rol': i.rol.name,
                'ci': i.ci,
                'birth': i.birth.strftime("%Y-%m-%d"),
                'qrprofile': i.qrprofile.url,
                "branch_user_id": i.branch_user_id,
                "branch_user": branch,
            }
            data.append(datas)
        # serializer=serializers.UserGetSerializer(data=data,many=True)
        return Response(data, status=status.HTTP_200_OK)


class UserProfile(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        datas = {}
        for i in image.objects.filter(user=request.user.id):
            print(i.user_id)
            users = User.objects.filter(id=i.user_id).values(
                'id', 'first_name', 'last_name', 'username', 'email')
            credit = Credits.objects.filter(
                user_id=i.user_id).values('id', 'number_credits')
            count_movies = Ticket.objects.filter(
                credits_ticket_id=credit[0]["id"]).count()
            count_survey = Survey.objects.filter(
                status=2, user_id=request.user.id).count()
            print(users)
            datas = {
                'id': users[0]['id'],
                'first_name': users[0]['first_name'],
                'last_name': users[0]['last_name'],
                'username': users[0]['username'],
                'email': users[0]['email'],
                'image': i.image.url,
                'qrprofile': i.qrprofile.url,
                'credit': credit[0]['number_credits'],
                'count_movies': count_movies,
                'count_survey': count_survey
            }
            data.append(datas)
        # serializer=serializers.UserGetSerializer(data=data,many=True)
        return Response(datas, status=status.HTTP_200_OK)


class LoginMovil(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for user in image.objects.filter(user=request.user.id):
            if user.type == "U":
                return Response({"user": True}, status=status.HTTP_200_OK)
            else:
                return Response({"user": False}, status=status.HTTP_403_FORBIDDEN)


class LoginWeb(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        for user in image.objects.filter(user=request.user.id):
            if user.type == "E":
                return Response({"Employee": True}, status=status.HTTP_200_OK)
            else:
                return Response({"Employee": False}, status=status.HTTP_403_FORBIDDEN)


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            # `django.contrib.auth.User` instance.
            'user': str(request.user.id),
            'auth': str(request.auth),  # None
        }
        return Response(content)


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication,
                              TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            if user.check_password(serializer.data['password']):
                user.set_password(serializer.data['new_password'])
                user.save()
                return Response({"change": True}, status=status.HTTP_200_OK)
            else:
                return Response({"password": "La contraseña anterior no es correcta", "change": False}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebMovilUSer(APIView):
    def post(self, request):
        serializer = serializers.QRSerializer(data=request.data)
        if serializer.is_valid():
            user_id = decrypt(serializer.data['qr'])
            data = []
            datas = {}
            for i in image.objects.filter(user_id=user_id):
                users = User.objects.filter(id=i.user_id).values(
                    'id', 'first_name', 'last_name', 'username', 'email')
                credit = Credits.objects.filter(
                    user_id=i.user_id).values('id', 'number_credits')
                count_movies = Ticket.objects.filter(
                    credits_ticket_id=credit[0]["id"]).count()
                count_survey = Survey.objects.filter(
                    status=2, user_id=request.user.id).count()
                print(users)
                datas = {
                    'id': users[0]['id'],
                    'first_name': users[0]['first_name'],
                    'last_name': users[0]['last_name'],
                    'username': users[0]['username'],
                    'email': users[0]['email'],
                    'image': i.image.url,
                    'qrprofile': i.qrprofile.url,
                    'credit': credit[0]['number_credits'],
                    'creidt_id': credit[0]['id'],
                    'count_movies': count_movies,
                    'count_survey': count_survey
                }
                data.append(datas)
            # serializer=serializers.UserGetSerializer(data=data,many=True)
            return Response(datas, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ROL

class RolList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rol = serializers.role.objects.all()
        serial = serializers.rolSerializer(rol, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
