import requests as req  #for OpenWeather API
import datetime 
import pytz


#files
import weatherTool_data as data
import speechtool as speech
import locations_onboot as boot
 


#PERSONAL VARS
weather_time_switch = 18  #prompt time that switches weather data from today to tomorrow in 24-hour time 
jacket_weather = 55  #temperature (f) that suggests a jacket
snowgear_cap = 30  #the amount of snow (mm) that requires you to bring snow gear



def startingLocations():
	""" Instantiates weather objects for list of starting locations"""
	for i in range(len(boot.locations)):
		name = list(boot.locations)[i]
		name = data.Location(boot.locations[list(boot.locations)[i]][0],boot.locations[list(boot.locations)[i]][1],boot.locations[list(boot.locations)[i]][2],boot.locations[list(boot.locations)[i]][3],boot.locations[list(boot.locations)[i]][4])
		locations.append(name)


def newLocation():
	""" This method prompts user on adding a new weather object location """
	city = input("What is the name of your new location?: ")
	zipcode = input("What is the 5 digit zipcode?: ")
	country = input("What is the country name?: ")  
	latitude = input("What is the latitude?: ") 
	longitude = input("What is the longitude?: ")
	new_loc = data.Location(city, zipcode, country, latitude, longitude)

	return new_loc     


def currentDescription(activeLocation):
	"""  This method calls live current data, and prints the location, current time, and temperature. """
	activeLocation.liveCall()  
	currentData = activeLocation.currentData()  # current data
	
	time = str(activeLocation._current_time_est_hour_12hour +" " + activeLocation._current_time_est_minute_12hour)  # code to give spoken time 
	if str(activeLocation._current_time_est_hour_12hour)[0] == "0":  
		time = str(activeLocation._current_time_est_hour_12hour)[-1] +" " + str(activeLocation._current_time_est_minute_12hour)

	speech.speak(speech.mimir, activeLocation._location+" at "+time+" eastern time currently feels like "+str(currentData[0])+"degrees and "+currentData[2])  # current description
	print(activeLocation._location+" at "+time+" eastern time currently feels like "+str(currentData[0])+" degrees and "+currentData[2])
	

def wearJacket(activeLocation): 
	""" This method calls live daily data and prints whether a jacket, an umbrella, or snow gear. """
	umbrella=0
	jacket=0
	snow=0

	activeLocation.liveCall()
	tomorrowData = activeLocation.tomorrowData()
	todayData = activeLocation.dailyData()

	if int(activeLocation._current_time_est[:2]) >= weather_time_switch:  # Setting jacket logic for tomorrow
		date = 'tomorrow'
		if tomorrowData[1] == "Snow" and (int(tomorrowData[-1]) > snowgear_cap):
			snow = 1
		else: 
			if tomorrowData[1] == "Rain":
				umbrella=1
			elif tomorrowData[0] < jacket_weather:
				jacket=1		
	elif int(activeLocation._current_time_est[:2]) < weather_time_switch:  # Setting jacket logic for today 
		date = 'today'
		if todayData[1] == "Snow" and int(todayData[-1]) > snowgear_cap:
			snow = 1
		else: 
			if todayData[1] == "Rain":
				umbrella = 1
			elif todayData[0] < jacket_weather:
				jacket = 1	

	if snow==1:  # snow decision 
		speech.speak(speech.mimir,"Bring snow gear "+date) 
		print("Bring snow gear "+date)
	else:
		if umbrella==1 and jacket==1:  # cold rain decision
			speech.speak(speech.mimir,"Bring a jacket and umbrella "+date)
			print("Bring a jacket and umbrella "+date)
		elif umbrella==1 and jacket==0:  # rain decision
			speech.speak(speech.mimir,"Bring an umbrella "+date)
			print("Bring an umbrella "+date)
		elif umbrella==0 and jacket==1:  # jacket decision
			speech.speak(speech.mimir,"Bring a jacket "+date)
			print("Bring a jacket "+date)
		else:
			if date == 'today':  # no jacket decision 
				speech.speak(speech.mimir, date+" is a nice "+ str(todayData[0]) + " degrees. You don't need a jacket.")
				print(date+" is a nice "+ str(todaydata[0]) + " degrees. You don't need a jacket.")
			elif date == 'tomorrow':  # no jacket decision
				speech.speak(speech.mimir, date+" will be a nice "+ str(tomorrowData[0]) + " degrees. You don't need a jacket.")
				print(date+" will be a nice "+ str(tomorrowdata[0]) + " degrees. You don't need a jacket.")




locations = []  # list of weather locations
startingLocations()	 # instantiates starting locations found in locations_onboot

# Prompting user to add new list of locations
kill = 0 
while kill==0:  
	prompt = input("Would you like to establish a new location?(y/n): ")
	while prompt != 'y' and prompt != 'n':  # logic to make y/n for new location robust
		print("")
		print("You must answer 'y' or 'n' to whether you would like to instantiate a new location.")
		prompt = input("Would you like to establish a new location?(y/n): ")

	if prompt == 'n':
		kill = 1
	elif prompt == 'y':
		locations.append(newLocation())


for i in locations:  # relays current description and jacket logic for each active location.
	currentDescription(i)
	wearJacket(i)


	



# NEED TO MAKE IT SO WEARJACKET ONLY ACCOUNTS FOR THE HOURS AFTER WHEN IT IS CALLED. If it rains in the morning and you call in the afternoon, 
# it will say you should bring a jacket but that is for the whole day not the part of the day left. 

# Errors being thrown in weatherTool_data when checking that daily data is taken at 11:00:00 est, if data in other countries for some reason

	





			


