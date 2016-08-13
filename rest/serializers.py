from rest_framework import serializers


class TubeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    loaded = serializers.BooleanField()


class LaunchingSystemerializer(serializers.Serializer):
    armed = serializers.BooleanField()
    tubes = TubeSerializer(many=True)
