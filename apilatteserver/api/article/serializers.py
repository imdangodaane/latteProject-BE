from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'badges', 'author']


class AllArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'