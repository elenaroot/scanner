from rest_framework import serializers

from scanner.models import Scan


class ScanSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    domain = serializers.CharField()

    class Meta:
        model = Scan
        fields = ['id', 'domain', 'state']

    def get_state(self, obj):
        return obj.get_state_display()

    def create(self, validated_data):
        instance, created = Scan.objects.get_or_create(**validated_data)
        return instance
