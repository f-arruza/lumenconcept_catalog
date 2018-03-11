import json, pika
from django.conf import settings
from .models import Offer
from .utils import send_message_rabbit, receive_message_rabbit
from background_task import background

@background(schedule=1)
def offer_verification():

    def callback(ch, method, properties, body):
        payload = json.loads(body.decode('utf-8'))
        try:
            order_code = payload['order_code']
            offers = payload['offers']
            success = "false"
            details = []

            if len(offers)==0:
                detail = {
                    "code": "0",
                    "error": "BAD_REQUEST"
                }
                details.append(detail)
            else:
                for offer in offers:
                    rs = Offer.objects.filter(code=offer['code'], active=True)
                    if len(rs)==0:
                        detail = {
                            "code": offer['code'],
                            "error": "NOT_FOUND"
                        }
                        details.append(detail)
                success = "true"
            response = {
                "order_code": order_code,
                "success": success,
                "details": details
            }
            # Enviar resultado de verificación a ORDER SERVICE
            send_message_rabbit('offer.verification.response', response)
            # Enviar solicitud de verificación a STOCK SERVICE
            # send_message_rabbit('stock.verification.request', body)
        except:
            print('ERROR')

    receive_message_rabbit('offer.verification.request', callback)
