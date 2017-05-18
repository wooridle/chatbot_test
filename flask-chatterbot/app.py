from flask import Flask, render_template, json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer



app = Flask(__name__)

english_bot = ChatBot("English Bot")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english")

chatterbot = ChatBot("Training Example")
chatterbot.set_trainer(ListTrainer)



#chatbot = ChatBot('Charlie')
chatbot = ChatBot("Johnny Five", read_only=True)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get/<string:query>")
def get_raw_response(query):
    return str(english_bot.get_response(query))


if __name__ == "__main__":
    app.run()
