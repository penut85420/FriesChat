import random
import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	else:
		output = request.get_json()
		for event in output['entry']:
			msging = event['messaging']
			for msg in msging:
				if msg.get('message'):
					recipient_id = msg['sender']['id']
					if msg['message'].get('text'):
						response_sent_text = get_message()
						send_message(recipient_id, response_sent_text)
					
					if msg['message'].get('attachments'):
						response_sent_nontext = get_message()
						send_message(recipient_id, response_sent_nontext)
	return "Msg Processed"

def verify_fb_token(token_sent):
	print(token_sent)
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return "Invalid verification token"

def send_message(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "Success"

def get_message():
	return "Yeeeeeeeeeeeeee"

if __name__ == '__main__':
	app.run()