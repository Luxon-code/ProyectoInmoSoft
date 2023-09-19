from rest_framework import serializers
from appInmoSoft.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','userCedula','userTelefono','userFoto','userTipo',
                  'username','email','first_name','last_name')