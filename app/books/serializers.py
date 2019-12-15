from rest_framework import serializers
from core.models import Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the books"""

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'volume', 'language', 'user']
        extra_kwargs = {'user': {'read_only': True}}
