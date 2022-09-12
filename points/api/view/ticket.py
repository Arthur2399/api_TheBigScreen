
from points.api.views import *
from survey import models as surveys

def createsurvey(user_id,movies,branch):
    try:
        template=surveys.Survey_template.objects.filter(state=1).first()
        fields={
                "suervey_template_id":template.id,
                "question1":template.question1,
                "question2":template.question2,
                "question3":template.question3,
                "question4":template.question4,
                "question5":template.question5,
                "movies_id":movies,
                "user_id_id":user_id,
                "branch_id":branch,
            }
        #print(fields)
        survey=surveys.Survey.objects.create(**fields)
        return True
    except Exception as e:
        print(str(e))
        return False

class template(APIView):
    def get(self, request):
        createsurvey()
        return Response({"message": "ok"})
class CreateTicket(APIView):
    def post(self,request):
        serializer=serializable.TicketsSerializers(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            fields={}
            template=False
            if serializer.data["credits_ticket"]!=None:
                print(serializer.data["credits_ticket"])
                user=""
                total=0
                for a in models.Credits.objects.raw("SELECT * FROM points_credits WHERE id=%s",[serializer.data["credits_ticket"]]):
                    user=a.user
                    total=a.number_credits
                    template=surveys.Survey_template.objects.filter(state=1).first()
                    if template==None:
                        vtemplate=False
                        fields={
                            "timetable_ticket_id":serializer.data["timetable_ticket_id"],
                            "value":serializer.data["value"],
                            "credits_ticket_id":None,
                            "name_user":None,
                            "totalcredit":None,
                            "balance":serializer.data["value"],
                            "qrImage":serializer.data["qrImage"],
                            "branch_ticket_id":serializer.data["branch_ticket"],
                            "date_functions":serializer.data["date_functions"]
                        }
                    else:
                        vtemplate=True
                        fields={
                            "timetable_ticket_id":serializer.data["timetable_ticket_id"],
                            "value":serializer.data["value"],
                            "credits_ticket_id":serializer.data["credits_ticket"],
                            "name_user":user,
                            "totalcredit":total,
                            "balance":total+serializer.data["value"],
                            "qrImage":serializer.data["qrImage"],
                            "branch_ticket_id":serializer.data["branch_ticket"],
                            "date_functions":serializer.data["date_functions"],
                            "state":2
                        }
                        serializable.models.Credits.objects.filter(id=serializer.data["credits_ticket"]).update(number_credits=fields["balance"])
                        movie_id=models.Timetable.objects.filter(id=fields["timetable_ticket_id"]).first().schedule_timetable.movies_schedule
                        user_id=models.Credits.objects.filter(id=fields["credits_ticket_id"]).first().user_id
                        createsurvey(user_id,movie_id,fields["branch_ticket_id"])
            else:
                template=surveys.Survey_template.objects.filter(state=1).first()
                if template==None:
                    vtemplate=False
                else:
                    vtemplate=True
                fields={
                    "timetable_ticket_id":serializer.data["timetable_ticket_id"],
                    "value":serializer.data["value"],
                    "credits_ticket_id":None,
                    "name_user":None,
                    "totalcredit":None,
                    "balance":serializer.data["value"],
                    "qrImage":serializer.data["qrImage"],
                    "branch_ticket_id":serializer.data["branch_ticket"],
                    "date_functions":serializer.data["date_functions"]
                }
            print(fields)
            #serializer.save()
            d=serializable.models.Ticket.objects.create(**fields)
            print(d.id)
            secret=encrypt(str(d.id))
            path="/ticket/"
            fil=str(d.id)+'.png'
            print (secret)
            Generator(secret,path,fil)
            serializable.models.Ticket.objects.filter(id=d.id).update(qrImage=path+fil)
            data=serializable.models.Ticket.objects.get(id=d.id)
            serializerdata=serializable.TicketsSerializers(data)
            return Response(serializerdata.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class ReadTicket(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        template=surveys.Survey_template.objects.filter(state=1).first()
        if template==None:
            return Response("No existe una plantilla de encuesta, no se puede registrar el ticket",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer=serializable.ReadTicketsSerializable(data=request.data)
        if serializer.is_valid():
            id=decrypt(serializer.data['qr'])
            user=request.user.id
            credit=serializable.models.Credits.objects.get(user=user)
            print(credit.number_credits)
            total=credit.number_credits
            control=serializable.models.Ticket.objects.filter(id=id)
            if len(control)==0:
                return Response("No existe el ticket",status=status.HTTP_400_BAD_REQUEST)
            ticket=serializable.models.Ticket.objects.get(id=id)
            if ticket.state==1:
                fields={
                    "timetable_ticket_id":ticket.timetable_ticket_id,
                    "value":ticket.value,
                    "credits_ticket_id":credit.id,
                    "name_user":credit.user.username,
                    "totalcredit":total,
                    "balance":total+ticket.value,
                    "qrImage":ticket.qrImage.url,
                    "branch_ticket_id":ticket.branch_ticket_id,
                    "date_functions":ticket.date_functions,
                    "date":ticket.date,
                    "state":2
                }
                print(fields)
                serializable.models.Credits.objects.filter(user=user).update(number_credits=fields["balance"])
                serializable.models.Ticket.objects.filter(id=id).update(**fields)
                movie_id=serializable.models.Timetable.objects.filter(id=fields["timetable_ticket_id"]).first().schedule_timetable.movies_schedule_id
                create=createsurvey(user,movie_id,fields["branch_ticket_id"])
                if create:
                    return Response("Registrado correctamente",status=status.HTTP_200_OK)
                else:
                    return Response("Los puntos se registro, pero no se creo la encuesta correctamente",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response("Ticket ya utilizado",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
