from flask import Flask, render_template, request, url_for
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'makjdrn94'
app.config['MYSQL_DATABASE_DB'] = 'Test'
app.config['MYSQL_DATABASE_host'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/verification',methods=['POST', 'GET'])
def auth():
    usr = request.form['name']
    passw = request.form['passw']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where userName ='" + usr + "' and password='" + passw + "'")
    data = cursor.fetchone()
    if data is None:
        return "False"
    else:
        return render_template('yourein.html')        
@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
