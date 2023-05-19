import argparse
BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
import json
from configparser import ConfigParser #
from urllib import parse, request,error
import sys
from pprint import pp
PADDING = 20
REVERSE = "\033[;7m"
RESET = "\033[0m"




#Step 2: Handle Secrets in Your Code
def _get_api_key():
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]
#Set Up an Argument Parser
def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    argname = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    argname.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )
    argname.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return argname.parse_args()
# Line 19 opens a conditional block after checking for Python’s "__main__" namespace, which allows you to
# define code that should run when you’re executing weather.py as a script.
# Line 20 calls read_user_cli_args(), effectively running the CLI parsing code logic you wrote further up.
#_______________________________________________________________________________________________________
# define the optional Boolean argument imperial. You set the action keyword argument to "store_true",
# which means that the value # for imperial will be True if users add the optional flag, and False if they don’t.
def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    print("URL :: ", url)
    return url
def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")

    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")
def diplay_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a city.

    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature

    More information at https://openweathermap.org/current#name
    """
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

   # print(f"{city}", end="")
   #  print(f"{city:^{PADDING}}", end="")
    print(f"{REVERSE}{city:^{PADDING}}{RESET}", end="")
    # print(f"\t{weather_description.capitalize()}", end=" ")
    print(
        f"\t{weather_description.capitalize():^{PADDING}}",
        end=" ",
    )
    print(f"({temperature}°{'F' if imperial else 'C'})")



if __name__ == "__main__":  #allows you to define code that should run when you’re executing weather.py as a script.
    user_args = read_user_cli_args()
    # print(user_args.city, user_args.imperial)
    query_url = build_weather_query(user_args.city, user_args.imperial)
    # print(query_url)
    weather_data = get_weather_data(query_url)
    # print(weather_data)
    # pp(weather_data)
    print(
        f"{weather_data['name']}: "
        f"{weather_data['weather'][0]['description']} "
        f"({weather_data['main']['temp']})"
    )
    diplay_weather_info(weather_data, user_args.imperial)



