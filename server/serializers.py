from django.contrib.auth.models import User, Group
from rest_framework import serializers
from server.models import Conta, Agencia, Transferencia


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AgenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agencia
        fields = ('nome_banco', 'numero',)


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ('nome_cliente', 'saldo_poupanca', 'saldo_corrente', 'agencia')


class TransferenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transferencia
        fields = ('conta_origem', 'conta_destino', 'data', 'tipo')
