from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class UsuarioSerializer(serializers.ModelSerializer):
    perfis = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "perfis"]

    def get_perfis(self, obj) -> list[str]:
        return sorted(obj.groups.values_list("name", flat=True))


class SaudeSerializer(serializers.Serializer):
    status = serializers.CharField()
