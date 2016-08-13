from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Index(APIView):
    def get(self, request):
        return Response("PRL 2016")


class Launch(APIView):
    def post(self, request):
        return Response("OK")
