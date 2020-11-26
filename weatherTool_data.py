import requests as req  #for OpenWeather API
import datetime 
import pytz



#OPENWEATHER VARS
KEY = "eac567b880fd463cdbc956e98d9dd1dd"




class Location:
	
	# lame to object
	_zipcode = ""
	_country = ""
	_latitude = ""
	_longitude = ""
	_location = ""
	_url_onecall = ""

	# live to object
	_data_onecall = ""
	_current_date = ""
	_current_numberday = ""
	_current_weekday = ""
	_current_time_est = ""
	_current_time_est_hour_12hour = ""
	_current_time_est_minute_12hour = ""



	def __init__(self, location, country, zipcode, latitude, longitude):
		self._zipcode = zipcode
		self._country = country
		self._latitude = latitude
		self._longitude = longitude
		self._location = location
		self._url_onecall ='https://api.openweathermap.org/data/2.5/onecall?lat='+self._latitude+'&lon='+self._longitude+'&appid='+KEY  # openweather url




	def liveCall(self):
		self._current_date = datetime.date.today()  # native current year-month-day 
		self._current_numberday = self._current_date.strftime('%d')  # native current day number 
		self.current_weekday = str(datetime.datetime.now().strftime('%A'))  # native current weekday 
		self._current_time_est = str(datetime.datetime.now().strftime('%X'))  # native current time in hours:minute:second
		self._current_time_est_hour_12hour = str(datetime.datetime.now().strftime('%I'))  # native current hour in 12 hour format
		self._current_time_est_minute_12hour = str(datetime.datetime.now().strftime('%M'))  # native current minute in 12 hour format
		self._data_onecall = (req.get(self._url_onecall)).json()  #as json->dictionary



	def currentData(self):
		current_time_unix_utc_weather = self._data_onecall['current']['dt']  # current unix dt in utc from openweather 
		current_date_weather = datetime.datetime.fromtimestamp(self._data_onecall['current']['dt'])  # current utc date from openweather
		current_time_est_weather = datetime.datetime.fromtimestamp(self._data_onecall['current']['dt']).strftime('%X')  # current est time from openweather
		if current_time_est_weather != self._current_time_est:  # ensuring that the current openweather and native est time are equal 
			delay_seconds = abs(int(current_time_est_weather[-2:])-int(self._current_time_est[-2:]))
			print("ERROR, openweather is not sourcing current time. Delay is "+str(delay_seconds)+" seconds. Check line 62 for more information")
		current_temp_f = int(((self._data_onecall['current']['temp'])-273.15)*(9/5)+32)  # current temperature 
		current_feelslike_f = int(((self._data_onecall['current']['feels_like'])-273.15)*(9/5)+32)  # current feels like temperature  
		current_precip = self._data_onecall['current']['weather'][0]['main']  # current precipitation
		current_description = self._data_onecall['current']['weather'][0]['description']  # current description 

		return current_feelslike_f, current_precip, current_description


	def dailyData(self):
		daily_time_unix_utc_weather = self._data_onecall['daily'][0]['dt']  # daily (4pm utc) unix dt in utc from openweather
		daily_date_weather = datetime.datetime.fromtimestamp(self._data_onecall['daily'][0]['dt'])  # daily (4pm utc) date from openweather
		daily_time_est_weather = datetime.datetime.fromtimestamp(self._data_onecall['daily'][0]['dt']).strftime('%X')  # daily time (11am est) from openweather
		if daily_time_est_weather != "11:00:00":  # ensuring that openweather is taking daily time at 11am est
			print("ERROR, openweather is not sourcing accurate time. Check line 76 for more information.")
		daily_temp_day_f = int(((self._data_onecall['daily'][0]['temp']['day'])-273.15)*(9/5)+32)  # daily (11am est) day temperature
		daily_feelslike_f = int(((self._data_onecall['daily'][0]['feels_like']['day'])-273.15)*(9/5)+32)  # daily (11am est) day feels like temperature  
		daily_precip = self._data_onecall['daily'][0]['weather'][0]['main']  # daily (11am est) precipitation 
		daily_description = self._data_onecall['daily'][0]['weather'][0]['description']  # daily (11am est) description 
		try:  #avoiding errors for rain/snow key 
			daily_rainvol = self._data_onecall['daily'][0]['rain']  # daily (11am est) rain volume
		except KeyError:
			daily_rainvol = None
			print('',end='')
		try:  #avoiding errors for rain/snow key 
			daily_snowvol = self._data_onecall['daily'][0]['snow']  # daily (11am est) snow volume
		except KeyError:
			daily_snowvol = None
			print('',end='')
		if int(self._current_numberday) != int(daily_date_weather.strftime('%d')):  #checking that the request pull is giving today's daily weather
			print("Weather request is not functioning properly. Check line 92 for more information.")

		return daily_feelslike_f, daily_precip, daily_description, daily_rainvol, daily_snowvol


	def tomorrowData(self):
		dailytom_time_unix_utc_weather = self._data_onecall['daily'][1]['dt']  #tomorrow daily unix dt from openweather
		dailytom_date_weather = datetime.datetime.fromtimestamp(self._data_onecall['daily'][1]['dt'])  # tomorrow daily (4pm UTC) date from openweather
		dailytom_time_est_weather = datetime.datetime.fromtimestamp(self._data_onecall['daily'][1]['dt']).strftime('%X')  # tomorrow daily time (11am est) from openweather
		if dailytom_time_est_weather != "11:00:00":
			print("ERROR, openweather is not sourcing accurate time. Check line 102 for more information.")
		dailytom_temp_day_f = int(((self._data_onecall['daily'][1]['temp']['day'])-273.15)*(9/5)+32)  # tomorrow daily (11am est) day temperature 
		dailytom_feelslike_f = int(((self._data_onecall['daily'][1]['feels_like']['day'])-273.15)*(9/5)+32)  # tomorrow daily (11am est) day feels like temperature
		dailytom_precip = self._data_onecall['daily'][1]['weather'][0]['main']  # tomorrow daily (11am est) precipitation
		dailytom_description = self._data_onecall['daily'][1]['weather'][0]['description'] 
		try: 
			dailytom_rainvol = self._data_onecall['daily'][1]['rain']  # tomorrow daily (11am est) rain volume 
		except KeyError:
			dailytom_rainvol = None
			print('',end='')
		try:
			dailytom_snowvol = self._data_onecall['daily'][1]['snow']  # tomorrow daily (11am est) snow volume
		except KeyError:
			dailytom_snowvol = None
			print('',end='')
		if int((self._current_date + datetime.timedelta(days=1)).strftime('%d')) != int(dailytom_date_weather.strftime('%d')):  #checking that the request pull is giving tomorrows's daily weather
			print("Weather request is not functioning properly. Check the weather tool file line 118 for more information.")

		return dailytom_feelslike_f, dailytom_precip, dailytom_description, dailytom_rainvol, dailytom_snowvol





