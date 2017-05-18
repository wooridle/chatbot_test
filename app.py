from flask import Flask, render_template, json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from konlpy.tag import Kkma


app = Flask(__name__)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/<string:query>")
def get_raw_response(query):
    return json.jsonify(str(chatterbot.get_response("good morning")))


@app.route('/get/chat/<string:query>')
def chat_response(query):
    kkma = Kkma()

    query_noun = kkma.nouns(query)
    response = None

    print(query_noun)
    if "안녕" in query_noun:
        response = '안녕하세요!'

    if "교열" and ("가격" or "견적") in query_noun:
        response = "3장 기준으로 5천원입니다.\n3장 이상의 경우에는 8천원입니다."

    return json.jsonify(response = response)


if __name__ == "__main__":
    chatterbot = ChatBot("baogao", read_only=True)
    chatterbot.set_trainer(ListTrainer)

    conversation = [
        "안녕",
        "안녕하세요"
    ]

    chatterbot.set_trainer(ListTrainer)
    chatterbot.train(conversation)

    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
    #app.run(host="0.0.0.0", port=5002, threaded=True)

