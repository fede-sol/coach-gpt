from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from historial.models import CoachedUser, CoachedUserIntro, ConsultAnswer, UserConsult
from .services import send_message
from .serializers import ConsultAnswerSerializer

class ReceiveMessage(APIView):
    def post(self, request):
        data = request.data

        if data.get("event") == "message":
            payload = data.get("payload", {})

            # Extraer el número de teléfono del campo "from"
            from_field = payload.get("from", "")
            phone_number = from_field.split("@")[0] if "@" in from_field else ""

            # Extraer el mensaje del campo "body"
            message = payload.get("body", "")

            print(f"Número: {phone_number}, Mensaje: {message}")

            user, created = CoachedUser.objects.get_or_create(phone_number=phone_number)

            if created:
                send_message(phone_recipient=phone_number, message='A que te dedicas? Que te gusta hacer fuera de tu vida profesional? Que problemas tenes que quieras mejorar?')
                return Response(status=status.HTTP_200_OK)
            else:
                user_consults_amount = UserConsult.objects.filter(user=user).count()


                if user_consults_amount == 1:
                    CoachedUserIntro.objects.create(user=user, user_intro=message)

                user_consult = UserConsult.objects.create(user=user, consult=message)
                try:
                    coached_user_intro = CoachedUserIntro.objects.get(user=user)
                except CoachedUserIntro.DoesNotExist:
                    coached_user_intro = None


            previous_consults = ConsultAnswer.objects.filter(user=user).order_by('id')

            previous_consults_serializer = ConsultAnswerSerializer(previous_consults, many=True)

            content_ia = {
                "previous_consults": previous_consults_serializer.data,
                "user_consult": user_consult.consult,
                "coached_user_intro": coached_user_intro.user_intro if coached_user_intro else None
            }

            print(content_ia)
            #message_send = generar_mensaje(user_consult)

            send_message(phone_recipient=phone_number, message=message)

        return Response({"message": "Hello, World!"})

