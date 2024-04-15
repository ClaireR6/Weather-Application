from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from mysite.models import User, Zip
import json, requests

api_key = "9a5b0c95772582be087f9c078715496e"

		
def get_weather_info(zipCode):
		url = "https://api.openweathermap.org/data/2.5/weather?units=imperial&zip="+str(zipCode)+"&appid="+api_key
	
		try:
			response = requests.get(url)
			response.raise_for_status(
			)  # Raise an exception for 4xx and 5xx status codes
	
			# Parse the JSON response
			data = response.json()
	
			# Extract relevant information from the response
			if data:
				return data
			else:
				print("No locations found.")
	
		except requests.exceptions.HTTPError as err:
			print(f"HTTP Error: {err}")
		except requests.exceptions.RequestException as err:
			print(f"Request Exception: {err}")
		except ValueError as err:
			print(f"Error parsing JSON: {err}")


# Create your views here.
class Home(View):

	def get(self, request):
		return render(request, 'index.html')


class UserView(View):

	def post(self, request):
		username = request.POST.get("user", None)
		user = User.objects.filter(username=username)

		if user:
			userZips = Zip.objects.filter(user=user)
			if len(userZips) > 0:
				for i in userZips:
					data = get_weather_info(i.code)
					if data['cod'] == 200:
						i.temp = data['main']['temp']
		else:
			user = User(username=user)
			user.save()
		#Json doesn't support tuples, so a list of
		#objects (dictionaries) is constructed to return
		ret = Zip.objects.filter(user=user).values()
		return JsonResponse(json.dumps(list(ret)),safe=False)


class ZipView(View):

	def post(self, request):
		username = request.POST.get("user", None)
		user = User.objects.filter(username=username)
		code = request.POST.get("code", None)

		if not user:
			user = User(username=username)
			user.save()
		else:
			user = User.objects.get(username=username)
		
		data = get_weather_info(code)
		if data['cod'] == 200:
			zipCode = Zip(user=user, code=code)
			temperature = data['main']['temp']
			print(temperature)
			zipCode.temp = temperature
			zipCode.save()

		ret = Zip.objects.filter(user=user).values()
		return JsonResponse(json.dumps(list(ret)),safe=False)


