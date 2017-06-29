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
    '''Essa classe é responável por manipular ações de conta do usuário
    A herança é feita de ModelViewSet que já contém implementações para
    GET, POST, DELETE e PUT.
    '''

    queryset = Conta.objects.all() #definimos qual será o modelo do BD a ser utilizado pela classe
    serializer_class = ContaSerializer #indicamos o serializer que manipula os dados json entre o request e python

    def update(self, request, *args, **kwargs):
        '''Método responsável por tratar de todas as requisões de PUT recebidas pelo servidor
        em especifico para a url /contas'''
        partial = kwargs.pop('partial', False)

        #operação de saque
        if request.data['tipo_op'] == 'saque':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            # inicio da seção critica
            lock = Lock()
            lock.acquire()  # will block if lock is already held
            try:
                self.sacar(request, serializer)
            finally:
                lock.release()

        # operação de deposito
        elif request.data['tipo_op'] == 'deposito':
            instance = Conta.objects.get(pk=request.data['conta_dest'])
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            #inicio da seção critica
            lock = Lock()
            lock.acquire()  # will block if lock is already held
            try:
                self.depositar(request, serializer)
            finally:
                lock.release()#destravamos a seção ciritica

        # operação de transferencia
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


    ## Metodos para manipular os dados das operacoes


    def sacar(self, request, serializer):
        valor_saque = request.data['valor_saque']#pegamos do request o valor de saque solicitado pelo cliente
        tipo_conta = request.data['tipo_conta']#tipo da conta sera Corrente ou Poupanca
        if tipo_conta == 'Corrente':
            novo_saldo = request.data['saldo_corrente'] - valor_saque#subtraimos o valor atual da conta pelo valor de saque solicitado pelo usuario
            if serializer.is_valid():
                serializer.save(saldo_corrente=novo_saldo)#o serializer se encarrega de enviar os dados json para o banco
            return valor_saque

        elif tipo_conta == 'Poupanca':#mesma operacao que a de cima porem para conta poupanca
            novo_saldo = request.data['saldo_poupanca'] - valor_saque
            if serializer.is_valid():
                serializer.save(saldo_poupanca=novo_saldo)
            return valor_saque

    def depositar(self, request, serializer):
        valor_deposito = request.data['valor_deposito']
        tipo_conta = request.data['tipo_conta']
        if tipo_conta == 'Corrente':
            novo_saldo = valor_deposito + request.data['saldo_corrente']#somamos o valor do deposito feito pelo cliente com o o saldo atual da conta
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

            conta_destino = Conta.objects.get(pk=request.data['conta_dest'])#buscamos no BD a conta destino da transf
            request.data['valor_saque'] = request.data['valor_transf']

            valor_transf = self.sacar(request, serializer)#realizamos um saque na conta origem e guardamos o valor para transf

            conta_destino.saldo_corrente = conta_destino.saldo_corrente + valor_transf#Somamos o saldo atual com o valor sacado da conta origem
            conta_destino.save()


        elif tipo_transf == 'Cc para P':#o mesmo procedimento realizado no codigo acima
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