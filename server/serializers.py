from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import Conta, Agencia

'''Serializers para manipular os dados entre json e framework django'''

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')#definimos os campos que serao enviados nos requests


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')#definimos os campos que serao enviados nos requests


class AgenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agencia
        fields = ('id', 'url', 'nome_banco', 'numero')#definimos os campos que serao enviados nos requests


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ('id', 'url', 'nome_cliente', 'saldo_poupanca', 'saldo_corrente', 'agencia')#definimos os campos que serao enviados nos requests
