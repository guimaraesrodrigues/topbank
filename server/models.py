from django.db import models


# Create your models here.
class Agencia(models.Model):
    nome_banco = models.CharField('nome do banco', max_length=20)
    numero = models.IntegerField()

    class Meta:
        verbose_name = 'agencia'
        verbose_name_plural = 'agencias'

    def __str__(self):
        return '{0.id} - {0.nome_banco}'.format(self)


class Conta(models.Model):
    nome_cliente = models.CharField('nome do cliente', max_length=100)
    saldo_corrente = models.FloatField(blank=True, null=True)
    saldo_poupanca = models.FloatField(blank=True, null=True)
    agencia = models.ForeignKey(Agencia, blank=True, null=True)

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'

    def __str__(self):
        return '{0.id} - {0.nome_cliente}'.format(self)


class Transferencia(models.Model):
    TIPOS = (
        ('cc', 'Conta corrente - Conta corrente'),
        ('cp', 'Conta corrente - Conta poupança'),
        ('doc', 'DOC'),
        ('ted', 'TED'),
    )

    conta_origem = models.ForeignKey(Conta, related_name='%(class)s_requests_created', blank=True, null=True)
    conta_destino = models.ForeignKey(Conta, blank=True, null=True)
    data = models.DateTimeField()
    tipo = models.CharField('tipos de transferencia', max_length=20, choices=TIPOS, default='')
