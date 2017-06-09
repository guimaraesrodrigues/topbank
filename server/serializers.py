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
        fields = ('id', 'url', 'nome_banco', 'numero')


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ('id', 'url', 'nome_cliente', 'saldo_poupanca', 'saldo_corrente', 'agencia')


class TransferenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transferencia
        fields = ('url', 'conta_origem', 'conta_destino', 'data', 'tipo')
