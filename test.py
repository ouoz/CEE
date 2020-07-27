import requests

def main():
    send_line_notify('てすとてすと')

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'lek07KeLPscS1odpzjdEB8A2l55pfrcIamyy20ydntk'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer {}'.format(line_notify_token)}
    data = {'message': 'message: {}'.format(notification_message)}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    main()