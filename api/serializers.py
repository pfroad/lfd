from api.models import SecretKey, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'mobile', 'name', 'birthday', 'sex', 'avatar', 'mail', 'city')