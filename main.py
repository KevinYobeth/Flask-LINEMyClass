import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction, URIAction
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'LDQyjg33LrsPBsHlmP9wSlyIGIz7Xb3R1DeIn2JeycXX5R6wmULu0Z0edX10ismW4PqM5MoavvFzNRm9f7JbbpKTdqRgLvA9KplzIQz+ozB+nvV2pQFWRONE0CvoBx6aqL9K1u5Y/NLJR/NVBEgcUgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('744ab32bb1452fa4ae4d52a6b571779e')

prefix = '#'
Database = {}


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == prefix + 'schedule':

        login_url = 'https://myclass.apps.binus.ac.id/Auth/Login'
        data = {
            'Username': 'leonardus.yobeth',
            'Password': 'passwordKevin25'
        }

        s = requests.Session()
        s.post(login_url, data)
        schdl = s.get(
            'https://myclass.apps.binus.ac.id/Home/GetViconSchedule')

        CarouselColumns = []
        for i in range(5):
            CarouselColumns.append(
                CarouselColumn(
                    thumbnail_image_url='https://i.postimg.cc/PryMxsk8/Frame-8-1.jpg',
                    title=schdl.json()[i]['CourseTitleEn'],
                    text='Meeting ID: ' +
                    schdl.json()[i]['MeetingId'] + '\nMeeting Password: ' +
                    schdl.json()[i]['MeetingPassword'],
                    actions=[
                        MessageAction(
                            label=schdl.json()[
                                i]['DisplayStartDate'],
                            text='Kelas ' + schdl.json()[i]['CourseTitleEn'] + ' woi jam ' +
                            schdl.json()[i]['StartTime'],
                        ),
                        URIAction(
                            label='Join Meeting',
                            uri=schdl.json()[i]['MeetingUrl'],
                        )
                    ]
                ),
            )

        carousel = TemplateSendMessage(
            alt_text='Class Schedule',
            template=CarouselTemplate(
                columns=CarouselColumns
            )
        )

        line_bot_api.reply_message(
            event.reply_token, carousel)

    # image_message = ImageSendMessage(
    #     original_content_url='https://narasi.klifonara.com/img/logo/logo-light.png',
    #     preview_image_url='https://narasi.klifonara.com/img/logo/logo-light.png'
    # )

    # line_bot_api.reply_message(
    #     event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
