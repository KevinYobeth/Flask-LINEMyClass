import os

import requests
from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (CarouselColumn, CarouselTemplate, ImageSendMessage,
                            JoinEvent, MessageAction, MessageEvent,
                            PostbackAction, TemplateSendMessage, TextMessage,
                            TextSendMessage, URIAction)

load_dotenv()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

prefix = '!'
Data = {}
login_url = 'https://myclass.apps.binus.ac.id/Auth/Login'


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
    chatType = event.source.type

    if msg.startswith(prefix + 'login'):

        msg = msg.split()

        if len(msg) < 3 or len(msg) > 3:
            line.reply_message(
                event.reply_token, TextSendMessage(text="Invalid Syntax!\nUse " + prefix + "login [username] [password] on private chat first\n\nExample:\n" + prefix + "login bambang.ferguso th1sp4wd"))
        else:
            if chatType == 'room':
                line.push_message(event.source.user_id, TextSendMessage(
                    text='Do not login on group chat! Unsent your username and password immediately!'))
                line.reply_message(
                    event.reply_token, TextSendMessage(text="Please check your private message!"))
            elif chatType == 'group':
                line.push_message(event.source.user_id, TextSendMessage(
                    text='Do not login on group chat! Unsent your username and password immediately!'))
                line.reply_message(
                    event.reply_token, TextSendMessage(text="Please check your private message!"))
            else:
                uid = event.source.user_id
                username = msg[1]
                password = msg[2]

                s = requests.Session()
                r = s.post(
                    login_url, {'Username': username, 'Password': password})

                if r.json()['Message'] == 'Login Success':
                    Data[uid] = {
                        'un': username,
                        'ps': password,
                    }
                    line.reply_message(
                        event.reply_token, TextSendMessage(text="You are logged in!"))
                else:
                    line.reply_message(
                        event.reply_token, TextSendMessage(text="Wrong username or password!"))

    if msg == prefix + 'sch':

        if event.source.user_id not in Data:
            line.reply_message(
                event.reply_token, TextSendMessage(text="Please use " + prefix + "login [username] [password] on private chat first\n\nExample:\n" + prefix + "login bambang.ferguso th1sp4wd"))
        else:
            data = {
                'Username': Data[event.source.user_id]['un'],
                'Password': Data[event.source.user_id]['ps']
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
                            MessageAction(
                                label=schdl.json()[
                                    i]['StartTime'] + " - " + schdl.json()[i]['EndTime'],
                                text='Kelas ' + schdl.json()[i]['CourseTitleEn'] + ' woi jam ' +
                                schdl.json()[i]['StartTime'],
                            ),
                            URIAction(
                                label='GSLC' if schdl.json(
                                )[i]['MeetingUrl'] == '-' else 'Join Meeting',
                                uri='https://binusmaya.binus.ac.id' if schdl.json(
                                )[i]['MeetingUrl'] == '-' else schdl.json()[i]['MeetingUrl'],
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

            line.reply_message(
                event.reply_token, carousel)

    if msg == prefix + 'schpc':

        if event.source.user_id not in Data:
            line.reply_message(
                event.reply_token, TextSendMessage(text="Please use " + prefix + "login [username] [password] on private chat first\n\nExample:\n" + prefix + "login bambang.ferguso th1sp4wd"))
        else:
            data = {
                'Username': Data[event.source.user_id]['un'],
                'Password': Data[event.source.user_id]['ps']
            }

            s = requests.Session()
            s.post(login_url, data)
            schdl = s.get(
                'https://myclass.apps.binus.ac.id/Home/GetViconSchedule')

            line.reply_message(
                event.reply_token, TextSendMessage(
                    text=schdl.json()[0]['DeliveryMode'] + " - " + schdl.json()[0]['CourseTitleEn'] + "\n" + schdl.json()[0]['DisplayStartDate'] + ", " + schdl.json()[0]['StartTime'] + " - " + schdl.json()[0]['EndTime'] + "\nMeeting ID: " + schdl.json()[0]['MeetingId'] + "\nMeeting Password: " + schdl.json()[0]['MeetingPassword'] + "\nMeeting Link: " + schdl.json()[0]['MeetingUrl'] + "\n\n" +
                    schdl.json()[1]['DeliveryMode'] + " - " + schdl.json()[1]['CourseTitleEn'] + "\n" + schdl.json()[1]['DisplayStartDate'] + ", " + schdl.json()[1]['StartTime'] + " - " + schdl.json()[1]['EndTime'] + "\nMeeting ID: " + schdl.json()[1]['MeetingId'] + "\nMeeting Password: " + schdl.json()[1]['MeetingPassword'] + "\nMeeting Link: " + schdl.json()[1]['MeetingUrl'] + "\n\n" +
                    schdl.json()[2]['DeliveryMode'] + " - " + schdl.json()[2]['CourseTitleEn'] + "\n" + schdl.json()[2]['DisplayStartDate'] + ", " + schdl.json()[2]['StartTime'] + " - " + schdl.json()[2]['EndTime'] + "\nMeeting ID: " + schdl.json()[2]['MeetingId'] + "\nMeeting Password: " + schdl.json()[2]['MeetingPassword'] + "\nMeeting Link: " + schdl.json()[2]['MeetingUrl'] + "\n\n" +
                    schdl.json()[3]['DeliveryMode'] + " - " + schdl.json()[2]['CourseTitleEn'] + "\n" + schdl.json()[3]['DisplayStartDate'] + ", " + schdl.json()[3]['StartTime'] + " - " + schdl.json()[3]['EndTime'] + "\nMeeting ID: " + schdl.json()[3]['MeetingId'] + "\nMeeting Password: " + schdl.json()[3]['MeetingPassword'] + "\nMeeting Link: " + schdl.json()[3]['MeetingUrl'] + "\n\n" +
                    schdl.json()[4]['DeliveryMode'] + " - " + schdl.json()[2]['CourseTitleEn'] + "\n" + schdl.json()[4]['DisplayStartDate'] + ", " + schdl.json()[4]['StartTime'] + " - " + schdl.json()[
                        4]['EndTime'] + "\nMeeting ID: " + schdl.json()[4]['MeetingId'] + "\nMeeting Password: " + schdl.json()[4]['MeetingPassword'] + "\nMeeting Link: " + schdl.json()[4]['MeetingUrl']
                ))

    if msg == prefix + 'leave':
        if chatType == 'room':
            line.reply_message(
                event.reply_token, TextSendMessage(text='Leaving Room!'))
            line.leave_room(event.source.room_id)

        elif chatType == 'group':
            line.reply_message(
                event.reply_token, TextSendMessage(text='Leaving Group!'))
            line.leave_group(event.source.group_id)

        else:
            line.reply_message(
                event.reply_token, TextSendMessage(text='MUAHHAHAHA you are stuck with me!'))

        line.reply_message(
            event.reply_token, TextSendMessage(text=event.source.type))

    if msg == prefix + 'help':
        line.reply_message(event.reply_token, TextSendMessage(
            text="DISCLAIMER: This is not an official MyClass BOT\n\nAvailable Commands:\n" + prefix + "help\n" + prefix + "login username password\n" + prefix + "sch\n" + prefix + "schpc\n" + prefix + "leave"))


@handler.add(JoinEvent)
def handle_follow(event):
    line.reply_message(event.reply_token, TextSendMessage(
        text="Hello! Thanks for adding me!\nDISCLAIMER: This is not an official MyClass BOT\n\nAvailable Commands:\n" + prefix + "help\n" + prefix + "login username password\n" + prefix + "sch\n" + prefix + "schpc\n" + prefix + "leave\n\nPs: Your password is not stored nor logged!"))


if __name__ == "__main__":
    app.run()
