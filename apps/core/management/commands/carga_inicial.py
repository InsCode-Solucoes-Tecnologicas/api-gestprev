"""Carga inicial: ente Natal e, so em desenvolvimento, um usuario Analista.

Pode rodar varias vezes: nada e duplicado.
"""

import os
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from apps.core import perfis
from apps.core.models import Ente

SIGLA = "NATALPREV"
NOME = "Instituto de Previdencia Social dos Servidores do Municipio do Natal"
CNPJ_DESENVOLVIMENTO = "0" * 14
USUARIO_DEV = "dev"


class Command(BaseCommand):
    help = "Cria o ente Natal e, com DJANGO_DEBUG=1, um usuario de desenvolvimento."

    def add_arguments(self, parser):
        parser.add_argument(
            "--cnpj",
            default=os.environ.get("ENTE_CNPJ", ""),
            help="CNPJ do ente (padrao: variavel ENTE_CNPJ).",
        )

    def handle(self, *args, **opcoes):
        self._ente(opcoes["cnpj"].strip())
        if settings.DEBUG:
            self._usuario_dev()
        else:
            self.stdout.write("DEBUG desligado: usuario de desenvolvimento nao criado.")

    def _ente(self, cnpj):
        ente = Ente.objects.filter(sigla=SIGLA).first()
        if ente:
            self.stdout.write(f"Ente {SIGLA} ja existe.")
            return
        if not cnpj:
            if not settings.DEBUG:
                raise CommandError("Informe o CNPJ do ente (--cnpj ou ENTE_CNPJ).")
            cnpj = CNPJ_DESENVOLVIMENTO
            self.stdout.write(self.style.WARNING("Sem ENTE_CNPJ: usando CNPJ ficticio."))
        if len(cnpj) != 14 or not cnpj.isdigit():
            raise CommandError("CNPJ deve ter 14 digitos, sem pontuacao.")
        Ente.objects.create(sigla=SIGLA, nome=NOME, cnpj=cnpj)
        self.stdout.write(self.style.SUCCESS(f"Ente {SIGLA} criado."))

    def _usuario_dev(self):
        modelo = get_user_model()
        if modelo.objects.filter(username=USUARIO_DEV).exists():
            self.stdout.write(f"Usuario {USUARIO_DEV} ja existe.")
            return
        senha = os.environ.get("DEV_USER_PASSWORD") or secrets.token_urlsafe(12)
        usuario = modelo.objects.create_user(username=USUARIO_DEV, password=senha)
        usuario.groups.add(Group.objects.get(name=perfis.ANALISTA))
        aviso = "" if os.environ.get("DEV_USER_PASSWORD") else f" Senha gerada: {senha}"
        self.stdout.write(self.style.SUCCESS(f"Usuario {USUARIO_DEV} (Analista) criado.{aviso}"))
