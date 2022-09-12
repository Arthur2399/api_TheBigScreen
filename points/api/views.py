from points import models
from utils.crypt import encrypt,decrypt
from utils.QrGenerator import Generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from points.api import serializable
from points.api.view.ticket import CreateTicket,ReadTicket,template
from points.api.view.awards import AwardsList,AwardsCreate
from points.api.view.transactions import TransactionCreate,prueba