from flask import Flask, render_template, request, url_for
from flaskext.mysql import MySQL
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

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
    splited = person.split()
    name = splited[0]
    surname = splited[1]

    message = open('Test', 'r').read()
    key = RSA.importKey(open('mypkey.der').read())
    signature = b64decode(sign)
    h = SHA512.new(message)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature):
        """ TODO Wyswietlanie dokumentu na ekranie """
        return render_template('yourein.html')
    else:
        return "Zle"
    
@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
