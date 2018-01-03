import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '507370070:AAFEDF3yeOWZtKIv3xS-Af4tE8q4GwvXnGo'
WEBHOOK_URL = 'https://bd3ffff8.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'START',
        'CNNALL',
        'BBCALL',
        'CNNURL',
        'BBCURL',
        'CNN10',
        'BBC10',
        'CNNURL_TRIV', #trivial
        'BBCURL_TRIV',
        'FREQ'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': [
                'START',
                'CNN10',
                'BBCALL',
                'BBC10',
                'CNNURL_TRIV',
                'BBCURL_TRIV'
            ],
            'dest': 'CNNALL',
            'conditions': 'is_going_to_CNNALL'
        },
        {
            'trigger': 'advance',
            'source': [
                'START',
                'BBC10',
                'CNNALL',
                'CNN10',
                'CNNURL_TRIV',
                'BBCURL_TRIV'
            ],
            'dest': 'BBCALL',
            'conditions': 'is_going_to_BBCALL'
        },
        {
            'trigger': 'advance',
            'source': [
                'START',
                'CNNALL',
                'BBCALL',
                'BBC10',
                'CNNURL_TRIV',
                'BBCURL_TRIV'
            ],
            'dest': 'CNN10',
            'conditions': 'is_going_to_CNN10'
        },
        {
            'trigger': 'advance',
            'source': [
                'START',
                'BBCALL',
                'CNNALL',
                'CNN10',
                'CNNURL_TRIV',
                'BBCURL_TRIV'
            ],
            'dest': 'BBC10',
            'conditions': 'is_going_to_BBC10'
        },
        { 
            'trigger': 'advance',
            'source': [
                'CNNALL',
                'CNN10',
                'CNNURL_TRIV'
            ],
            'dest': 'CNNURL',
            'conditions': 'is_going_to_CNNURL'
        },
        { 
            'trigger': 'advance',
            'source': [
                'BBCALL',
                'BBC10',
                'BBCURL_TRIV'
            ],
            'dest': 'BBCURL',
            'conditions': 'is_going_to_BBCURL'
        },
        {
            'trigger': 'go_triv',
            'source': 'CNNURL',
            'dest': 'CNNURL_TRIV'
        },
        {
            'trigger': 'go_triv',
            'source': 'BBCURL',
            'dest': 'BBCURL_TRIV'
        },
        { 
            'trigger': 'advance',
            'source': [
                'START',
                'CNNALL',
                'CNN10',
                'CNNURL_TRIV',
                'BBCALL',
                'BBC10',
                'BBCURL_TRIV'
            ],
            'dest': 'FREQ',
            'conditions': 'is_going_to_FREQ'
        },
        {
            'trigger': 'go_start',
            'source': 'FREQ',
            'dest': 'START'   
        }
    ],
    initial='START',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run(port=5487)
