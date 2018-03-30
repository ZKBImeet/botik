from flask import Flask

app = Flask(__name__)
app.config.from_object('credentials')

#from botik import main_bot1

