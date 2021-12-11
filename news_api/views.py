from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HackerNewsItemSerializer
from news.models import HackerNewsItem


class HackerNewsItemSerializerViews(APIView):
    def get(self, request, id=None):
        if id:
            item = HackerNewsItem.objects.get(id=id)
            serializer = HackerNewsItemSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = HackerNewsItem.objects.all()
        serializer = HackerNewsItemSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HackerNewsItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if id > 100000:
            return Response({"status": "error", "data": "Thou shall not edit items that thou did not create"})
        item = HackerNewsItem.objects.get(id=id)
        serializer = HackerNewsItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        if id > 100000:
            return Response({"status": "error", "data": "Thou shall not delete items that thou did not create"})
        item = get_object_or_404(HackerNewsItem, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})