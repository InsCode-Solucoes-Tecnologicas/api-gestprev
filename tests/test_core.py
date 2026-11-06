import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.core import perfis


@pytest.fixture
def cliente():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def usuario(db):
    u = get_user_model().objects.create_user(username="analista", password="senha-forte-123")
    u.groups.add(Group.objects.get(name=perfis.ANALISTA))
    return u


def test_saude_sem_login(cliente):
    resposta = cliente.get("/api/saude/")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


@pytest.mark.django_db
def test_perfis_criados_pela_migracao():
    assert set(Group.objects.values_list("name", flat=True)) >= set(perfis.TODOS)


@pytest.mark.django_db
def test_eu_exige_login(cliente):
    assert cliente.get("/api/auth/eu/").status_code == 403


def _login(cliente, senha):
    cliente.get("/api/auth/csrf/")
    token = cliente.cookies["csrftoken"].value
    return cliente.post(
        "/api/auth/login/",
        {"username": "analista", "password": senha},
        format="json",
        HTTP_X_CSRFTOKEN=token,
    )


def test_login_sessao_e_eu(cliente, usuario):
    resposta = _login(cliente, "senha-forte-123")
    assert resposta.status_code == 200
    assert resposta.json()["perfis"] == [perfis.ANALISTA]

    eu = cliente.get("/api/auth/eu/")
    assert eu.status_code == 200
    assert eu.json()["username"] == "analista"


def test_login_senha_errada(cliente, usuario):
    assert _login(cliente, "errada").status_code == 400


def test_login_sem_csrf_recusado(usuario):
    cliente = APIClient(enforce_csrf_checks=True)
    resposta = cliente.post(
        "/api/auth/login/", {"username": "analista", "password": "senha-forte-123"}, format="json"
    )
    assert resposta.status_code == 403


@pytest.mark.django_db
def test_schema_openapi(cliente, usuario):
    cliente.force_authenticate(usuario)
    resposta = cliente.get("/api/schema/", HTTP_ACCEPT="application/json")
    assert resposta.status_code == 200
