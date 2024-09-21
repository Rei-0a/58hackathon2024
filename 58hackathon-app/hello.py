# ====== FlaskでHello Worldを表示 ======
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

# 実行
if __name__ == '__main__':
    app.run()