from flask import Flask, render_template, request, send_file, jsonify
from deepzoom import start_deepzoom
import os
import string
from PIL import Image
import io
from flask_cors import CORS
import random
import base64
from create_mosaic import mosaic
import requests

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/second')
def second():
    return render_template('./second.html')

@app.route("/upload", methods=['POST'])
def upload():
    data = request.json
    print(data['email'])
    if data['img']:
        user_im_name = id_generator()
        im_user = Image.open(io.BytesIO(base64.b64decode(data['img'])))
        if im_user.mode in ("RGBA", "P"):
            im_user = im_user.convert("RGB")
        im_user.save("test/"+user_im_name+".jpg")
        mosaic("test/"+user_im_name+".jpg", "foto_win/")
    return jsonify({
        "img": "https://40207b8e.ngrok.io/img?filename="+user_im_name+".jpg"
    })

@app.route('/img')
def img():
    filename = request.args.get('filename')
    return send_file('output/test/'+filename, attachment_filename='python.jpg')

if __name__ == '__main__':
    app.run()
