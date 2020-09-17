from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question


# Create your views here.
class HelloWorldView(APIView):
    def get(self, request):  
        JSONSerializer = serializers.get_serializer('json')
        json_serializer = JSONSerializer()
        json_serializer.serialize(Question.objects.all())
        data = json_serializer.getvalue()
        return Response({'message': 'Hello, world!',
                         'questions': data})
