import json
import http.client
from config import *


def send_whatsapp_message(to_number, template_id, placeholders, images):
    try:
        conn = http.client.HTTPSConnection(INFOBIP_BASE_URL)

        payload = {
            "messages": [
                {
                    "from": INFOBIP_WHATSAPP_NUMBER,
                    "to": to_number,
                    "content": {
                        "templateName": template_id,
                        "templateData": {
                            "body": {
                                "placeholders": placeholders
                            }
                        },
                        "language": "en_GB"
                    },
                    "imageUrls": images
                }
            ]
        }

        headers = {
            'Authorization': f'APP {INFOBIP_AUTHORIZATION_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        payload_json = json.dumps(payload)

        conn.request("POST", "/whatsapp/1/message/template", payload_json, headers)
        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            response_data = json.loads(data.decode("utf-8"))

            if 'messages' in response_data:
                # Successful response
                message_status = response_data['messages'][0]['status']
                if message_status['groupId'] == 1 and message_status['name'] == 'PENDING_ENROUTE':
                    return True, 'WhatsApp message sent successfully.'
                else:
                    return False, f'Failed to send WhatsApp message. Unexpected status: {message_status}'
            else:
                return False, 'Failed to send WhatsApp message. Unexpected response structure.'

        else:
            # Handle different failure scenarios
            response_error = json.loads(data.decode("utf-8"))
            if 'requestError' in response_error and 'serviceException' in response_error['requestError']:
                error_message = response_error['requestError']['serviceException']['text']
                return False, f'Failed to send WhatsApp message. Error: {error_message}'
            else:
                return False, f'Failed to send WhatsApp message. Unexpected error response.'

    except http.client.HTTPException as http_exception:
        return False, f'HTTP Exception: {http_exception}'
    except ConnectionError as connection_error:
        return False, f'Connection Error: {connection_error}'
    except Exception as generic_exception:
        return False, f'An unexpected error occurred: {generic_exception}'
