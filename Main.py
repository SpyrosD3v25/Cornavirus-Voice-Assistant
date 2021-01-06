"""
Spyros Chatziargyros, 1 jun of 2021
"""

import requests
import json
import pyttsx3
import speech_recognition as sr
import re


##
#Required Info
API_KEY = "t-pLZN99PqzA"
PROJECT_TOKEN = "taOLsbN_gUkv"
RUN_TOKEN = "tzVb-NzTBZZG"
##

#############################################################
class Data:
	def __init__(self, api_key, project_token):
		self.api_key = api_key
		self.project_token = project_token
		self.params = {
			"api_key": self.api_key
		}
		self.get_data()
	########	
	def get_data(self):
		response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
		self.data = json.loads(response.text)
	########	
	def get_total_cases(self):
		data = self.data['total']

		for content in data:
			if content['name'] == 'Coronavirus Cases:':
				return content['value']

		return "0"
	########			
	def get_total_deaths(self):
		data = self.data['total']

		for content in data:
			if content['name'] == 'Deaths:':
				return content['value']

		return "0"
	########	
	def get_country_data(self, country):
		data = self.data["country"]

		for content in data:
			if content['name'].lower() == country.lower():
				return content

		return "0"

	def get_all_coutries(self):
		countries = []
		for country in self.data['country']:
			countries.append(country['name'].lower())

		return countries

#############################################################

########
def speak(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()
########

########
def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
		except Exception as e:
			print("Exception: ", str(e))

	return said.lower()
########

########
def main():
	print("Started Program")
	END_PHRASE = "stop"
	data = Data(API_KEY, PROJECT_TOKEN)
	country_list = data.get_all_coutries()

	TOTAL_PATTERNS = {
					re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
					re.compile("[\w\s]+ total cases+ [\w\s]"): data.get_total_cases,
					re.compile("[\w\s]+ total [\w\s]+ cases+ [\w\s]"): data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
					re.compile("total cases+ [\w\s]"): data.get_total_cases,
					re.compile("total cases"): data.get_total_cases,

					re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
					re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
					re.compile("[\w\s]+ total deaths+ [\w\s]"): data.get_total_deaths,
					re.compile("[\w\s]+ total [\w\s]+ deaths+ [\w\s]"): data.get_total_deaths,
					re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
					re.compile("total deaths+ [\w\s]"): data.get_total_deaths,
					re.compile("total deaths"): data.get_total_deaths
	}

	COUNTRY_PATTERNS = {
					re.compile("[\w\s]+ [\w\s]+ cases"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("[\w\s]+ cases"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("[\w\s]+ cases+ [\w\s]"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("[\w\s]+ [\w\s]+ cases+ [\w\s]"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("[\w\s]+ cases"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("cases+ [\w\s]"): Lambda country: data.get_country_data(country)['total_cases'],
					re.compile("cases"): Lambda country: data.get_country_data(country)['total_cases'],

					re.compile("[\w\s]+ [\w\s]+ deaths"): Lambda country: data.get_country_data(country)['total_deaths'],
					re.compile("[\w\s]+ deaths"): Lambda country: data.get_country_data(country)['total cases'],
					re.compile("[\w\s]+ deaths+ [\w\s]"): Lambda country: data.get_country_data(country)['total_deaths'],
					re.compile("[\w\s]+ [\w\s]+ deaths+ [\w\s]"): Lambda country: data.get_country_data(country)['total_deaths'],
					re.compile("[\w\s]+ deaths"): Lambda country: data.get_country_data(country)['total_deaths'],
					re.compile("deaths+ [\w\s]"): Lambda country: data.get_country_data(country)['total_deaths'],
					re.compile("deaths"): Lambda country: data.get_country_data(country)['total_deaths'],
	}

	while True:
		print("Listening: ")
		text = get_audio()
		print(text)
		result = None

		for pattern, func in COUNTRY_PATTERNS.items():
			if pattern.match(text):
				words = set(text.split(" "))
				for country in country_list:
					if country in words:
						result = func(country)
						break

		for pattern, func in TOTAL_PATTERNS.items():
			if pattern.match(text):
				result = func()
				break

		if result:
			speak(result)

		if text.find(END_PHRASE) != -1:
			print("Exiting")
			break
########

main()