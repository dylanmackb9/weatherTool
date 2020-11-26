import pyttsx3  #texttospeech


# List of good voice IDs 
	#7 male robotic
	#10 female robotic higher
	#17 female smooth australian
	#19 female portuguese
	#20 female scandanavian
	#26 female nice, american
	#27 female russian/polish
	#28 female american firm 
	#32 female robotic 
	#36 female firm british
	#37 male french robotic
	#39 female indian
	#45 male russian



print("Initializing Mimir...")
mimir = pyttsx3.init()
voices = mimir.getProperty('voices')
mimir.setProperty('voice', voices[7].id) 
mimir.setProperty('rate', 200)
print("Mimir on standby.")
print()


def speak(engine,text):
	engine.say(text)
	engine.runAndWait()









	









