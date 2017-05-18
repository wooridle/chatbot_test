from flask import Flask, render_template, json, make_response, request
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


@app.route('/chat', methods = ['GET'])
def chat_response(query):
    kkma = Kkma()
    query = request.args.get('q')
    #query = query.decode('cp949').encode('utf-8')
    query_noun = kkma.nouns(query)
    response = None
    print(query_noun)
    if "안녕" in query_noun:
        response = '안녕하세요!'

    if "교열" and ("가격" or "견적") in query_noun:
        response = "3장 기준으로 5천원입니다.\n3장 이상의 경우에는 8천원입니다."

    return json.jsonify(response = response)

def pretranslatedCreateFile(self, project_id, resource_id):
    """
    파일 업로드 API

    **Parameters**
      #. **"project_id"**: 프로젝트 ID (URL)
      #. **"resource_id"**: Resource ID (URL)
      #. **"preview_permission"**: 미리보기 권한
      #. **"file_list[]"**: 파일 목록

    **Response**
      #. **200**: 게시 성공

        .. code-block:: json
           :linenos:

           {
             "resource_id": 1 // Request ID
           }

      #. **410**: 게시 실패 

    """
    pretranslatedObj = Pretranslated(g.db)
    parameters = ciceron_lib.parse_request(request)
    upload_files = request.files.getlist("file_list[]")
    parameters['project_id'] = project_id
    parameters['resource_id'] = resource_id

    for upload_file in upload_files:
        parameters['file_name'] = upload_file.filename
        parameters['file_binary'] = upload_file.read()
        is_ok, file_id = pretranslatedObj.createFile(**parameters)
        if is_ok == False:
            g.db.rollback()
            return make_response("Fail", 410)

    else:
        g.db.commit()
        return make_response("OK", 200)


def _insert(self, table, **kwargs):
    cursor = self.conn.cursor()
    query_tmpl = """
        INSERT INTO CICERON.{table}
        ({columns})
        VALUES
        ({prepared_statements})
    """
    columns = ','.join( list( kwargs.keys() ) )
    prepared_statements = ','.join( ['%s' for _ in list(kwargs.keys())] )
    query = query_tmpl.format(
                table=table
              , columns=columns
              , prepared_statements=prepared_statements
              )

    try:
        cursor.execute(query, list( kwargs.values() ) )
    except Exception:
        traceback.print_exc()
        self.conn.rollback()
        return False

    return True

if __name__ == "__main__":
    # chatterbot = ChatBot("baogao", read_only=True)
    # chatterbot.set_trainer(ListTrainer)
    #
    # conversation = [
    #     "안녕",
    #     "안녕하세요"
    # ]
    #
    # chatterbot.set_trainer(ListTrainer)
    # chatterbot.train(conversation)

    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
    #app.run(host="0.0.0.0", port=5002, threaded=True)

