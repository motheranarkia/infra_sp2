from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Comment, Category, Genre, Title, Review


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('id', 'category', 'genre', 'rating')

    def get_rating(self, obj):
        return obj.review_title.all().aggregate(average=Avg('score'))[
            'average'
        ]


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(
        slug_field='username', read_only=True,
    )
    score = serializers.IntegerField()

    def validate(self, data):
        if self.context['request'].method == 'POST' and Review.objects.filter(
                title=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение!',
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class WriteTitleSerializer(ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'
