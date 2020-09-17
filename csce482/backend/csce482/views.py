from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from datetime import datetime 

from exampleapp.models import Question

# Two examples of how view functions can be created

class HelloWorldView(APIView):
    def get(self, request):  
        JSONSerializer = serializers.get_serializer('json')
        json_serializer = JSONSerializer()
        json_serializer.serialize(Question.objects.all())
        data = json_serializer.getvalue()
        return Response({'message': 'Hello, world!',
                         'questions': data})

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def create_question(request):
    question = Question(question_text='Question 4?', pub_date=datetime.now())
    question.save()
    return Response({'success': True})