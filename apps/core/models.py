from django.db import models


class Ente(models.Model):
    """Municipio/RPPS atendido. Toda entidade de negocio aponta para um ente (multi-ente)."""

    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=30, unique=True)
    cnpj = models.CharField(max_length=14, unique=True)
    adaptador_dados = models.CharField(
        max_length=50,
        default="planilha",
        help_text="Adaptador da fonte de dados em uso (ex.: folha, planilha).",
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.sigla
