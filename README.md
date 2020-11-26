
WeatherTool uses openweather's free weather API to gather weather data from around the globe and relay information to the user.  


Using the One Call API, a single call grabs current, hourly, and 7 day daily weather forecasts based on longitude and latitude position. 
WeatherTool_data creates a weather location object, which contains all the information and forecast data about a specified location. This allows weather forecast data in multiple locations to be accessed at the same time. 

WeatherTool_data utilizes a class method liveCall() which, when called, pulls live data from the One Call API, so all weather forecasts can be tracked live.

weatherTool_main contains functions startingLocations(), newLocation(), currentDescription(), wearJacket(). 
	
	startingLocations() takings location data from locations_onboot and instantiates these locations on calling WeatherTool_main, so that these locations need not be added manually by the user. 

	newLocation() allows the user to add a new location object to the list of locations by inputing location data. 

	currentDescription() takes a location as an input, and uses liveCall() to and speechtool to relay the current weather 

	wearJacket() takes a location as an input, and uses liveCall() to decide whether a jacket, umbrella or snow gear should be used at the current location for that day. 


Lastly, speechtool ties all of weatherTool's capability together using pyttsx3, a text to speech python library. This way, the program relays information to the user in through both the shell and audibly. 

More functionality to come..



