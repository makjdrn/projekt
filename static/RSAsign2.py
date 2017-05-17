from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from base64 import b64encode
from flask import Flask
from flaskext.mysql import MySQL
import sys
from Tkinter import *

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'makjdrn94'
app.config['MYSQL_DATABASE_DB'] = 'Podpisy_Database'
app.config['MYSQL_DATABASE_host'] = 'localhost'
mysql.init_app(app)

""" Plik podawany w lini komend """
    
class App(Frame):
    def __init__(self, master):
        Frame.__init__(self,master, width=400, height=200, bg="white")

        self.w = Label(master, text="Imie:")
        self.w.pack()

        self.imie = Entry(master)
        self.imie.pack(fill=X)

        self.w = Label(master, text="Nazwisko:")
        self.w.pack()

        self.nazwisko = Entry(master)
        self.nazwisko.pack(fill=X)

        self.w = Label(master, text="Nazwa pliku:")
        self.w.pack()

        self.plik = Entry(master)
        self.plik.pack(fill=X)

        self.imie.focus_set()
        self.nazwisko.focus_set()
        self.plik.focus_set()

        self.b = Button(master, text="get", width=10, command=self.add)
        self.b.pack(side=BOTTOM)
    def add(self):
        name = self.imie.get()
        surname = self.nazwisko.get()
        filename = self.plik.get()
        message = open(filename, 'r').read()
        print "hello"
        """ Generowanie klucza """

        key = RSA.generate(2048)
        f = open('PrivateKey.pem', 'w')
        f.write(key.exportKey('PEM'))
        f.close()
        f = open('PublicKey.pem', 'w')
        f.write(key.publickey().exportKey('PEM'))
        f.close()

        key = RSA.importKey(open('PublicKey.pem').read())
        pubKey = open('PublicKey.pem').read()
        """ Podpisywanie """

        key = RSA.importKey(open('PrivateKey.pem').read())
        privKey = open('PrivateKey.pem').read()
        h = SHA512.new(message)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        sign = b64encode(signature)

        try:
            cursor = mysql.connect().cursor()
        except mysql.Error:
            child = Tk()
            frame = Frame(child, width = 100, height = 100, bg = "white")
            w = Label(child, text="Problem przy polaczeniu z baza danych")
            w.pack()
            b = Button(child, text="Powrot", width = 10, command=clear)

        print name + surname + filename            
        cursor.execute("INSERT INTO Podpisy (Name, Surname, Sign, PrivateKey, PublicKey, DocName) values ('" + name + "','" + surname + "','" + sign + "'" + ",'" + privKey + "'" + ",'" + pubKey + "'," + "'" + filename + "')")
        cursor.connection.commit()
        cursor.connection.close()

        self.imie.delete(0, 'end')
        self.nazwisko.delete(0, 'end')
        self.plik.delete(0, 'end')

def main():
    root = Tk()
    App(root).pack()
    root.mainloop()

if __name__ == "__main__":
    main()

""" f = open('signature.cer', 'w')
f.write(b64encode(signature))
f.close() """


