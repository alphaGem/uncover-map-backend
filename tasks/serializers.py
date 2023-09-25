from rest_framework import routers,serializers,viewsets
from .models import Info
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Info
        fields = [
            'id',
            'name',
            'professionalType',
            'attitudeType',
            'isVerify',
            'hospital',
            'position',
            'department',
            'province',
            'city',
            'address',
            'longtitude',
            'latitude',
            'avatarUrl',
            'contacts',
            'comments',
            'source']


