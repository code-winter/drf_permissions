from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        owner = self.context["request"].user
        method = self.context['request'].method
        adv_obj = Advertisement.objects.filter(creator=owner)
        adv_opened = adv_obj.filter(status='OPEN').count()
        if method == 'POST' and adv_opened >= 10:
            raise serializers.ValidationError('Слишком много открытых объявлений!')
        if method == 'PATCH':
            if data.get('status') == 'OPEN' and adv_opened >= 10:
                raise serializers.ValidationError('Слишком много открытых объявлений!')
        return data
