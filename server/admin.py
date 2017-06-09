from django.contrib import admin
from .models import Conta, Agencia, Transferencia

admin.site.register(Conta)
admin.site.register(Agencia)
admin.site.register(Transferencia)