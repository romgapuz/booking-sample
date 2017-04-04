from pyfcm import FCMNotification
from utils.config import read_config


class PushSender(object):
    """
    from utils.push_notification import PushSender
    registration_id = "cxrVJNtYbQ4:APA91bHAom5YOuSH7PalfWEj61ZjYKrzu8Q9LzuW9-sOnxWP1tX9jtWCiujfRJ5crdVxA8xmjsem_00V1z54MOg0tRrg4bsJo5mBoola-DeA2f4-WOFVQK7nQVQTw8CVfN0S5rmseVJH"
    title = "eKonek"
    message = "Testing"
    ps = PushSender()
    ps.send_single_notification(registration_id, title, message)
    """
    
    def send_single_notification(self, registration_id, title, message):
        # get config entries
        config = read_config()
        server_key = config.get('fcm', 'server_key')
        
        push_service = FCMNotification(api_key=server_key)
        result = push_service.notify_single_device(
            registration_id=registration_id,
            message_title=title,
            message_body=message
        )

        print result
