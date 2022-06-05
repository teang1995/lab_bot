# -*- coding: utf-8 -*-
import os
import json
import requests

from flask import Flask, request, make_response, jsonify
from slacker import Slacker
from dotenv import load_dotenv

load_dotenv(verbose=True)

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
ROOT_URL = os.getenv('ROOT_URL')

token = SLACK_TOKEN #여기를 변경 해주세요
root_url = ROOT_URL

slack = Slacker(token)
app = Flask(__name__)


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_answer(user_query):
    command = user_query.split(' ')[1]
    if command == 'nvidia-smi':
        server_num = user_query.split(' ')[2]
        gpu_status = {}
        url = f'http://{root_url}{server_num}:5002/check_gpu'
        response = requests.get(url)
        res = response.json()

        results = res['result']
        for i, result in enumerate(results):
            gpu_name = result['name']
            memory_total = result['memory.total']
            memory_used = result['memory.used']
            memory_free = result['memory.free']
            gpu_status[i] = {'gpu_name': gpu_name,
                             'memory_total': memory_total,
                             'memory_used': memory_used,
                             'memory_ratio': (int(memory_used) * 100) / int(memory_total)}
            
        answer =  json.dumps(gpu_status, indent=2)

    else:
        answer = user_query



    return answer


def event_handler(event_type, slack_event):

    channel = slack_event["event"]["channel"]

    string_slack_event = str(slack_event)
    print(string_slack_event)
    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:  # 멘션으로 호출

        try:

            user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']

            answer = get_answer(user_query)

            post_message(token, channel, answer)

            return make_response("ok", 200, )

        except IndexError:

            pass



    message = "[%s] cannot find event handler" % event_type

    return make_response(message, 200, {"X-Slack-No-Retry": 1})





@app.route('/test', methods=['POST'])

def hello_there():
    
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:

        # return jsonify(slack_event['challenge'])
        return make_response("healthy", 200)

    if "event" in slack_event:

        event_type = slack_event["event"]["type"]

        return event_handler(event_type, slack_event)

    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

@app.route('/', methods=['GET'])

def heath_check():
    return make_response("healthy", 200)

@app.route('/', methods=['POST'])

def heath_check2():
    return make_response("healthy2", 200)



if __name__ == '__main__':

    app.run(debug=True)