from points.api.views import *

def detail(detail,header):
    for k in detail:
        k["transaction_detail"]=header
        #print(k)
        serializableDetail=serializable.TransactionsDetailSerializable(data=k)
        if serializableDetail.is_valid():
            serializableDetail.save()
        else:
            return serializableDetail.errors
    return True

class TransactionCreate(APIView):
    def post(self, request):
        serializerheader= serializable.TransactionsSerializable(data=request.data["header"])
        if serializerheader.is_valid():
            header=serializerheader.save()
            print(header.id)
            details=request.data["detail"]
            det=detail(details,header.id)
            if det==True:
                models.Credits.objects.filter(pk=header.credits_translation.id).update(number_credits=header.balance)
                return Response("ok",status=status.HTTP_200_OK)
            else:
                return Response(det,status=status.HTTP_400_BAD_REQUEST)   
        return Response(serializerheader.errors,status=status.HTTP_400_BAD_REQUEST)
            
class prueba(APIView):
    def post(self,request):
        serializer=serializable.TransactionPrincipalSerializable(data=request.data)
        try:
            if serializer.is_valid():
                header= serializable.TransactionsSerializable(data=serializer.data["header"])
                if header.is_valid():
                    header.save()
                    header_id=header.data["id"]
                    details=detail(serializer.data["detail"],header_id)
                    if details==True:
                        models.Credits.objects.filter(pk=header.data["credits_translation"]).update(number_credits=header.data["balance"])
                    print(header_id)
                    return Response("OK",status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)