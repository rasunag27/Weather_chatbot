from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import bs4
import os
from flask import make_response
import json
import urllib.request
from bs4 import BeautifulSoup

# import pyowm
# from weather import processRequest
# from output.intent import get_facts

app = Flask(__name__)
api_key = '2579bd51c63fc4f77d5421274f7bc71e'


# owm = pyowm.OWM(apikey)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    #print(json.dumps(req, indent=4))
    intent = req.get('queryResult').get('intent').get('displayName')

    if intent == 'weather_intent':

        city = req.get('queryResult').get('parameters').get('cityName')

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key).read()
        list_of_data = json.loads(source)

        data = {
            "cityname": str(city),
            "temp_k": str(list_of_data.get('main').get('temp')),
            #"temp_c": "temp_k".get() - 273.15,
            "humidity": str(list_of_data.get('main').get('humidity')) + '%'
        }
        temp_c = round((float(data.get("temp_k")) - 273.15),2)
        data['temp_c'] = str(temp_c) + 'c'
        #print(data)
        result = "Today the weather in " + data['cityname'] + " is: \n" \
                 + "Humidity : " + data['humidity'] \
                 +".\nTemp in celsius : " + data['temp_c']


        print(result)
        return{'fulfillment': result}
    else:
        return{'fulfillment': 'Intent not matched'}


if __name__ == '__main__':
    app.run(debug=True)
