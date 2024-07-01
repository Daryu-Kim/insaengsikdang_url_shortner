import random
import string
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import ShortUrl
from .serializers import ShortUrlSerializer

class ShortUrlViewSet(viewsets.ModelViewSet):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortUrlSerializer

    def create(self, request, *args, **kwargs):
        # 단축 URL 생성
        short_url = self.generate_short_url(request.data['original_url'])

        # 데이터베이스에 저장
        serializer = self.get_serializer(data={'short_url': short_url, 'original_url': request.data['original_url']})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        # 단축 URL을 입력하면 원본 URL로 리다이렉트
        short_url = kwargs['pk']
        try:
            short_url_obj = ShortUrl.objects.get(short_url=short_url)
            return redirect(short_url_obj.original_url)
        except ShortUrl.DoesNotExist:
            return Response({'error': 'Invalid short URL'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def generate_short_url(self, original_url):
        # 6자리 랜덤 문자열 생성
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # 단축 URL이 이미 존재하는지 확인
        while ShortUrl.objects.filter(short_url=short_url).exists():
            short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        return short_url