from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=200)),
                ("sigla", models.CharField(max_length=30, unique=True)),
                ("cnpj", models.CharField(max_length=14, unique=True)),
                (
                    "adaptador_dados",
                    models.CharField(
                        default="planilha",
                        help_text="Adaptador da fonte de dados em uso (ex.: folha, planilha).",
                        max_length=50,
                    ),
                ),
                ("ativo", models.BooleanField(default=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["nome"]},
        ),
    ]
