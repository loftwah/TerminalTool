from core.models import Book
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from . import serializers
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'title'

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user)
