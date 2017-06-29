from django.db import models

'''Modelos do Banco de dados'''
# Create your models here.
class Agencia(models.Model):
    nome_banco = models.CharField('nome do banco', max_length=20)
    numero = models.IntegerField()

    class Meta:
        verbose_name = 'agencia'
        verbose_name_plural = 'agencias'

    def __str__(self):
        return '{0.id} - {0.nome_banco}'.format(self)

'''Um mesmo numero de conta pode conter conta corrente e conta poupança'''
class Conta(models.Model):
    nome_cliente = models.CharField('nome do cliente', max_length=100)
    saldo_corrente = models.FloatField(blank=True, null=True)
    saldo_poupanca = models.FloatField(blank=True, null=True)
    agencia = models.ForeignKey(Agencia, blank=True, null=True)#foreign key para a tabela agencia

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'

    def __str__(self):
        return '{0.id} - {0.nome_cliente}'.format(self)