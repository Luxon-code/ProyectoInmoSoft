from rest_framework import serializers
from appInmoSoft.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','userCedula','userTelefono','userFoto','userTipo',
                  'username','email','first_name','last_name')
        
class ClienteInteresadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteInteresado
        fields = ('id','cliNombre','cliApellido','cliCedula','cliCorreo','cliTelefono','cliProyecto')
