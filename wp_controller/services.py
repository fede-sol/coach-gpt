import requests


from django.conf import settings

def send_message(*, phone_recipient : str, message : str):

    url = f"{settings.WP_API_URL}/api/sendText"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "chatId": f"{phone_recipient}@c.us",
        "text": message,
        "session": "default"
    }

    response = requests.post(url, json=data, headers=headers)

    result = response.json()

    if result.get("status") != 200:
        raise Exception(f"Error sending message: {result}")


