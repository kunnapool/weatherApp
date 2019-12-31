import requests
import json
from datetime import datetime

def get_weather(city, country_code):

    def to_c(k):
        """
        Kelvin -> Celsius
        """
        return k - 273

    # kunnapool@gmail.com
    API_KEY = '23d81feec8af8fdd6d29a99bf9ab6af8'

    API_ENDPOINT = 'http://api.openweathermap.org'
    API_CALL = "{end_point}/data/2.5/forecast?q={city_name},{country_code}&mode=json&APPID={key}".format(end_point=API_ENDPOINT,
                                                                                                               city_name=city,
                                                                                                               country_code=country_code,
                                                                                                               key=API_KEY)


    # API call and convert to json
    req = requests.get(API_CALL).json()

    # API return format from documentation:
    # https://openweathermap.org/forecast5
    today_name = datetime.fromtimestamp(req['list'][0]['dt']).strftime('%A')
    
    today_weather = []
    this_day = today_name
    next_days_weather = []
    
    list_idx = 0
    while list_idx < len(req['list']):
        
        # what day in list
        day_name = datetime.fromtimestamp(req['list'][list_idx]['dt']).strftime('%A')
        weather_avg = 0.0
        weather_num = 0
        this_day = day_name

        # if today, collect 3-hourly data
        if day_name == today_name:
            today_weather.append(req['list'][list_idx])

        # otherwise, get average temp
        else:
            # until same day
            while list_idx < len(req['list']) and day_name == this_day:
                weather_avg += req['list'][list_idx]['main']['temp']
                weather_num += 1
                day_name = datetime.fromtimestamp(req['list'][list_idx]['dt']).strftime('%A')
                list_idx += 1

            weather_avg = weather_avg/weather_num
            next_days_weather.append(dict(Day=this_day, Temp=to_c(weather_avg)))

        list_idx += 1

    return today_name, next_days_weather