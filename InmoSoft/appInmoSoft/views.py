from datetime import date, datetime
from django.shortcuts import render, redirect
from appInmoSoft.models import *
from django.contrib.auth.models import Group
from django.db import Error, transaction
import random
import string
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
import urllib
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count

# Create your views here.
def vistaRegistrarUsuario(request):
    return render(request,'administrador/registrarUsuario.html')