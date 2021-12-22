#linebot用のファイル ここに色々移す

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import ssl
import datetime
import subprocess
import shutil

BASE_DIR=Path(__file__).resolve().parent #ベースのパス
UPLOAD_FOLDER=BASE_DIR / "public" / "images" #保存先パス
app = Flask(__name__,static_folder="public") #appにわたす
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER #uploadフォルダ定義

#get set token
YOUR_CHANNEL_ACCESS_TOKEN = "TNRYWQMMkF26vnoKeYj3RqV4/4zsW7Nq4OcLVpfifMlRKoOWn7v0t6dX7st04oO3bcvS0GGEI7l3wCptMJ+osm/G5YR1jNssjASFYU+90bltrZdoGmm6niiAjbMdn0IfguUkM4eHt9EQeT7E8xCYYgdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "b393f2e01e79bd59b4459c03673deba3"
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

time2="" #グローバル変数じゃないほうがいいかも

def get_picture():
    time=datetime.datetime.now()
    time2=str(time.year)+"-"+str(time.month)+"-"+str(time.day)+" "+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+".jpg"
    cheese=['fswebcam','-p','MJPEG','-r','1280x720','--no-banner','-D','1',time2]
    try:
        subprocess.check_call(cheese)
        shutil.move(time2,UPLOAD_FOLDER)
        print ("Command finished.")
        

    except:
        return "Command envailed."


#herokuへのデプロイが成功したかどうかを確認する
@app.route("/")
def hello_world():
    return "hello world!"


#LINE DevelopersのWebhookにURLを指定してWebhookからURLにイベントが送られる
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数
    try:
        handler.handle(body, signature)
        get_picture()
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#以下でWebhookから送られてきたイベントをどのように処理する
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



# ポート番号の設定
if __name__ == "__main__":
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context = ('fullchain.pem', 'privkey.pem') #渡す形式はpemファイルだよ
    port = 4567 #int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port,ssl_context=context,threaded=True,debug=True)