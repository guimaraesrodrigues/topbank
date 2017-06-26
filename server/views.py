from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import Conta, Agencia, Transferencia
from server.serializers import UserSerializer, GroupSerializer, ContaSerializer, AgenciaSerializer, TransferenciaSerializer

class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # ipdb; ipdb.set_trace()
        tipo_conta = request.data['tipo_conta']

        if request.data['tipo_op'] == 'saque':
            self.sacar(request, serializer, tipo_conta)
        elif request.data['tipo_op'] == 'deposito':
            self.depositar(request, serializer, tipo_conta)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def sacar(self, request, serializer, tipo_conta):
        valor_saque = request.data['valor_saque']
        if tipo_conta == 'Corrente':
            novo_saldo = request.data['saldo_corrente'] - valor_saque
            if serializer.is_valid():
                serializer.save(saldo_corrente=novo_saldo)
        elif tipo_conta == 'Poupanca':
            novo_saldo = request.data['saldo_poupanca'] - valor_saque
            if serializer.is_valid():
                serializer.save(saldo_poupanca=novo_saldo)

    def depositar(self, request, serializer, tipo_conta):
        valor_deposito = request.data['valor_deposito']
        if tipo_conta == 'Corrente':
            novo_saldo = valor_deposito + request.data['saldo_corrente']
            if serializer.is_valid():
                serializer.save(saldo_corrente=novo_saldo)
        elif tipo_conta == 'Poupanca':
            novo_saldo = valor_deposito + request.data['saldo_poupanca']
            if serializer.is_valid():
                serializer.save(saldo_poupanca=novo_saldo)



class AgenciaViewSet(viewsets.ModelViewSet):
    queryset = Agencia.objects.all()
    serializer_class = AgenciaSerializer

    def update(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        return super().update(request, args, kwargs)




class TransferenciaViewSet(viewsets.ModelViewSet):
    queryset = Transferencia.objects.all()
    serializer_class = TransferenciaSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ContaList(APIView):
    def get(self, request):
        contas = Conta.objects.all()
        serializer = ContaSerializer(contas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
