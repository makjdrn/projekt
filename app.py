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
    splited = person.split()
    name = splited[0]
    surname = splited[1]

    message = open('Test.pdf', 'r').read()
    key = RSA.importKey(open('mypkey.der').read())
    signature = b64decode(sign)
    h = SHA512.new(message)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature):
        """ TODO Wyswietlanie dokumentu na ekranie """
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT DocName FROM Podpisy WHERE Sign = '" + sign + "'")
        DocName = cursor.fetchone()
        DocName = ''.join(DocName)
        cursor.execute("SELECT DocPath FROM Podpisy WHERE Sign = '" + sign + "'")
        DocPath = cursor.fetchone()
        DocPath = ''.join(DocPath)
        filePath = DocPath + "/" + DocName
        """ content = DocName """
        
        
        fileName = "'" + DocName + "'"
        with Image(filename='Test.pdf') as img:
            with img.convert('jpg') as converted:
                converted.save(filename='Test.jpg')
        """ return send_file(f, attachment_filename='Test.pdf') """
        """ return render_template("yourein.html", content=filePath) """
        m = re.match(r'(.*)', 'Test-.jpg')
        return render_template("yourein.html", content=m)
    else:
        return "Zle"
@app.route('/verification/<content>')
def show_pdf(docs=None):
    f = open('/home/pi/Desktop/Server/Test.pdf', "rb")
    response = make_response(f)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'Test.pdf'
    return response
    
@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

if __name__ == '__main__':
    app.run(debug=True, threaded = True,host='0.0.0.0')
