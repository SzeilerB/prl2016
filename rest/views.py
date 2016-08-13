from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LaunchingSystemerializer
from .models import LaunchingSystem


prl = LaunchingSystem()


class Index(APIView):
    def get(self, request):
        return Response("PRL 2016")


class Armer(APIView):
    def post(self, request):
        prl.armed = True
        return Response(status=status.HTTP_200_OK)


class DisArmer(APIView):
    def post(self, request):
        prl.armed = False
        return Response(status=status.HTTP_200_OK)


class LauncherStatus(APIView):
    def get(self, request):
        return Response(LaunchingSystemerializer(prl).data)
