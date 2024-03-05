from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *

app = Flask(__name__)
@app.route("/")
def home():   
    rtTrips = getRealTimeTripUpdates()
    return getAllTrips(rtTrips) #TODO create html and use rendertemplate


if __name__ == "__main__":
    app.run(debug=True)
    
