import json
from flask import Flask, request, make_response
 
app = Flask(__name__)
 
@app.route('/test', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5002)