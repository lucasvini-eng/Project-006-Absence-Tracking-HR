from django.db import models


class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True, related_name="funcionarios"
    )
    gestor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="liderados"
    )
    saldo_ferias_dias = models.PositiveIntegerField(default=30)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"


class TipoAusencia(models.Model):
    nome = models.CharField(max_length=80, unique=True)  # Férias, Atestado, Licença, etc.
    remunerada = models.BooleanField(default=True)
    exige_anexo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class StatusAusencia(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    APROVADA = "APROVADA", "Aprovada"
    REJEITADA = "REJEITADA", "Rejeitada"
    CANCELADA = "CANCELADA", "Cancelada"


class Ausencia(models.Model):
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, related_name="ausencias"
    )
    tipo = models.ForeignKey(TipoAusencia, on_delete=models.PROTECT)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias_solicitados = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=StatusAusencia.choices, default=StatusAusencia.PENDENTE
    )
    aprovado_por = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="aprovacoes"
    )
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.funcionario.nome} - {self.tipo.nome} ({self.status})"
