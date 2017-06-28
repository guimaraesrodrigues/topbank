from threading import Lock

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

        if request.data['tipo_op'] == 'saque':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            self.sacar(request, serializer)

        elif request.data['tipo_op'] == 'deposito':
            instance = Conta.objects.get(pk=request.data['conta_dest'])
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            self.depositar(request, serializer)

        elif request.data['tipo_op'] == 'transf':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            lock = Lock()
            lock.acquire()  # will block if lock is already held
            try:
                self.transferir(request, serializer)
            finally:
                lock.release()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def sacar(self, request, serializer):
        valor_saque = request.data['valor_saque']
        tipo_conta = request.data['tipo_conta']
        if tipo_conta == 'Corrente':
            novo_saldo = request.data['saldo_corrente'] - valor_saque
            if serializer.is_valid():
                serializer.save(saldo_corrente=novo_saldo)
            return valor_saque

        elif tipo_conta == 'Poupanca':
            novo_saldo = request.data['saldo_poupanca'] - valor_saque
            if serializer.is_valid():
                serializer.save(saldo_poupanca=novo_saldo)
            return valor_saque

    def depositar(self, request, serializer):
        valor_deposito = request.data['valor_deposito']
        tipo_conta = request.data['tipo_conta']
        if tipo_conta == 'Corrente':
            novo_saldo = valor_deposito + request.data['saldo_corrente']
            if serializer.is_valid():
                serializer.save(saldo_corrente=novo_saldo)
            return valor_deposito

        elif tipo_conta == 'Poupanca':
            novo_saldo = valor_deposito + request.data['saldo_poupanca']
            if serializer.is_valid():
                serializer.save(saldo_poupanca=novo_saldo)
            return valor_deposito

    def transferir(self, request, serializer):
        tipo_transf = request.data['tipo_transf']
     
        if tipo_transf == 'Cc para Cc':
            request.data['tipo_conta'] = 'Corrente'

            conta_destino = Conta.objects.get(pk=request.data['conta_dest'])
            request.data['valor_saque'] = request.data['valor_transf']

            valor_transf = self.sacar(request, serializer)

            conta_destino.saldo_corrente = conta_destino.saldo_corrente + valor_transf
            conta_destino.save()


        elif tipo_transf == 'Cc para P':
            request.data['tipo_conta'] = 'Corrente'

            conta_destino = Conta.objects.get(pk=request.data['conta_dest'])
            request.data['valor_saque'] = request.data['valor_transf']

            valor_transf = self.sacar(request, serializer)

            conta_destino.saldo_poupanca = conta_destino.saldo_poupanca + valor_transf
            conta_destino.save()

        elif tipo_transf == 'DOC':
            request.data['tipo_conta'] = 'Corrente'

            conta_destino = Conta.objects.get(pk=request.data['conta_dest'])
            request.data['valor_saque'] = request.data['valor_transf']

            valor_transf = self.sacar(request, serializer)

            conta_destino.saldo_poupanca = conta_destino.saldo_poupanca + valor_transf
            conta_destino.save()

        elif tipo_transf == 'TED':
            request.data['tipo_conta'] = 'Corrente'

            conta_destino = Conta.objects.get(pk=request.data['conta_dest'])
            request.data['valor_saque'] = request.data['valor_transf']

            valor_transf = self.sacar(request, serializer)

            conta_destino.saldo_poupanca = conta_destino.saldo_poupanca + valor_transf
            conta_destino.save()




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
