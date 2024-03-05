from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
