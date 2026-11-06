import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.core.models import Ente


@pytest.mark.django_db
def test_rodar_duas_vezes_nao_duplica(settings, monkeypatch):
    settings.DEBUG = True
    monkeypatch.setenv("DEV_USER_PASSWORD", "senha-dev-123")
    call_command("carga_inicial", "--cnpj", "12345678000199")
    call_command("carga_inicial", "--cnpj", "12345678000199")
    assert Ente.objects.filter(sigla="NATALPREV").count() == 1
    usuario = get_user_model().objects.get(username="dev")
    assert usuario.groups.filter(name="Analista").exists()
    assert usuario.check_password("senha-dev-123")


@pytest.mark.django_db
def test_sem_debug_nao_cria_usuario(settings):
    settings.DEBUG = False
    call_command("carga_inicial", "--cnpj", "12345678000199")
    assert Ente.objects.filter(sigla="NATALPREV").exists()
    assert not get_user_model().objects.filter(username="dev").exists()


@pytest.mark.django_db
def test_sem_debug_exige_cnpj(settings):
    settings.DEBUG = False
    with pytest.raises(CommandError):
        call_command("carga_inicial", "--cnpj", "")


@pytest.mark.django_db
def test_cnpj_invalido(settings):
    settings.DEBUG = True
    with pytest.raises(CommandError):
        call_command("carga_inicial", "--cnpj", "12.345.678/0001-99")
