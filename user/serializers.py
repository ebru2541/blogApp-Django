from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            # "password",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        ]

#! password şifreli yazabilmek için
    def validate(self, attrs):
        from django.contrib.auth.password_validation import validate_password # doğrulama fonksiyonu
        from django.contrib.auth.hashers import make_password # şifreleme fonksiyonu
        password = attrs['password'] # Password al.
        validate_password(password) # Validation'dan geçir.
        attrs.update(
            {
                'password': make_password(password) # Password şifrele ve güncelle.
            }
        )
        return super().validate(attrs) # Orjinal methodu çalıştır.
