from flask import Flask, render_template, request, url_for, send_file, make_response
from flaskext.mysql import MySQL
from gevent.wsgi import WSGIServer
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from wand.image import Image
import re

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'makjdrn94'
app.config['MYSQL_DATABASE_DB'] = 'Podpisy_Database'
app.config['MYSQL_DATABASE_host'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/verification',methods=['POST', 'GET'])
def auth():
    sign = request.form['sign']
    person = request.form['person']
    while True:
        try:
            splited = person.split()
            name = splited[0]
            surname = splited[1]
            break
        except IndexError:
            return render_template("login_error.html")

    try:
        cursor = mysql.connect().cursor()
    except mysql.Error:
        return render_template("database_error.html")
    cursor.execute("SELECT DocName FROM Podpisy WHERE Sign = '" + sign + "' and Name = '" + name + "' and Surname = '" + surname + "'")
    DocName = cursor.fetchone()
    if DocName is None:
        return render_template("login_error.html")
    else:
        DocName = ''.join(DocName)

    cursor.execute("SELECT PublicKey FROM Podpisy WHERE Sign = '" + sign + "' and Name = '" + name + "' and Surname = '" + surname + "'")
    pubkey = cursor.fetchone()

    message = open("/home/pi/Desktop/Server/static/" + DocName, 'r').read()
    key = RSA.importKey(pubkey)
    signature = b64decode(sign)
    h = SHA512.new(message)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature):
        return render_template("yourein.html", content=DocName)
    else:
        return "Zle"


if __name__ == '__main__':
    app.run(debug=False, threaded = True,host='0.0.0.0')
