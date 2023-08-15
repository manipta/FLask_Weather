import requests as r
import configparser
from flask import Flask, render_template, request

# __name__ will be replaced by name of py file that is app
app = Flask(__name__)
app.debug=True
@app.route('/')
def weather_dashboard():
    return render_template('home.html')


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['api_keys']['open_weather']


def get_weather_results(zip_code, api_key, temp, country_code="in"):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={},{}&units={}&appid={}".format(
        zip_code, country_code, temp, api_key)
    print(api_url)
    result = r.get(api_url)
    return result.json()


@app.route('/results', methods=['POST'])  # telling method is a post method
def result_page():
    zipCode = request.form['zipCode']
    countryCode = request.form['countryCode']
    tempin = request.form['temp']
    if countryCode != "":
        data = get_weather_results(zipCode, get_api_key(), tempin, countryCode)
    else:
        data = get_weather_results(zipCode, get_api_key(), tempin)
    temp="{0:.2f}".format(data["main"]["temp"])
    feels_like_temp= "{0:.2f}".format(data["main"]["feels_like"])
    temp_min= "{0:.2f}".format(data["main"]["temp_min"])
    temp_max= "{0:.2f}".format(data["main"]["temp_max"])
    if(tempin=="imperial"):
        unit="F"
    else:
        unit="C"
    Weather=data["weather"][0]["main"]
    loc=data["name"]+", "+data["sys"]["country"]
    result=render_template("results.html",temp=temp,feels_like_temp=feels_like_temp
                           ,temp_max=temp_max,temp_min=temp_min,unit=unit,Weather=Weather
                           ,loc=loc)
    return result

if __name__ == '__main__':
    app.run(debug=True)  # will run app once
