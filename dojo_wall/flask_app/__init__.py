from flask import Flask, session
app = Flask(__name__)
app.secret_key = "French toast apocalypse, Yeah!!!" 

# The secret key is needed to run session
# This is one thing that would usually be kept in your git ignored file, along with API keys