from django.db import models

# Create your models here.

class Conta(models.Model):
	nome_cliente = models.CharField('nome do cliente', max_length=100)
	saldo = models.FloatField()

	class Meta:
		verbose_name = 'conta'
		verbose_name_plural = 'contas'

	def __str__(self):
		return '{0.id} - {0.nome_cliente}'.format(self)