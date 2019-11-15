from rest_framework import serializers
from .models import ItemDb


class ItemDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDb
        fields = '__all__'