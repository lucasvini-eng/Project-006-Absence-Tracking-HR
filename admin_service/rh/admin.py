from django.contrib import admin

from .models import Departamento, Funcionario, TipoAusencia, Ausencia


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cargo", "departamento", "gestor", "saldo_ferias_dias", "ativo")
    list_filter = ("departamento", "ativo")
    search_fields = ("nome", "email")


@admin.register(TipoAusencia)
class TipoAusenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "remunerada", "exige_anexo")


@admin.register(Ausencia)
class AusenciaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "funcionario", "tipo", "data_inicio", "data_fim",
        "dias_solicitados", "status", "aprovado_por",
    )
    list_filter = ("status", "tipo")
    search_fields = ("funcionario__nome",)
    date_hierarchy = "data_inicio"
