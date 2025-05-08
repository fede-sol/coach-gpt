from rest_framework import serializers
from historial.models import ConsultAnswer, UserConsult

class UserConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConsult
        fields = '__all__'



class ConsultAnswerSerializer(serializers.ModelSerializer):
    consult = UserConsultSerializer()
    class Meta:
        model = ConsultAnswer
        fields = ['id', 'consult', 'answer']


