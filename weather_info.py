import requests
import re
import locations
import logging
import logger
import app_config
from bs4 import BeautifulSoup
from typing import Optional


# Initializing the logger
logger.init_logger()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logger.LOG_LEVEL)


class Data:
    radian: float = 57.29577

    def __init__(self):
        self.uv_info = dict()
        self.clouds_info = dict()
        self.uv_index: Optional[float] = None
        self.uv_index_accu: Optional[float] = None
        self.ozone_level: Optional[float] = None
        self.safe_exposure_time = None
        self.sun_azimuth_openuv: Optional[float] = None
        self.sun_altitude_openuv: Optional[float] = None
        self.cloud_ceiling = None
        self.cloud_cover = None
        self.sky: Optional[str] = None
        self.precipitation: Optional[float] = None
        self.cloud_opacity = None

    @staticmethod
    def get_sun_info(city):
        """
        Fetches sun altitude from https://www.timeanddate.com/sun/ and extract info from HTML
        :param city:    string. Name of a city which appears in 'locations' dictionary for example: London, Tirana, etc
        :return:        tuple. sun_azimuth: float + string  ,  sun_altitude: float
                        None
        """
        country = locations.locations[city]['Country']
        try:
            url = f'https://www.timeanddate.com/sun/{country}/{city}'
            LOGGER.info(f'Fetching sun altitude from: {url}')
            response = requests.get(url, verify=False)
            if response.status_code != 200:
                LOGGER.warning(f'Did not receive a proper status code: {response.status_code}')
                return None

            soup = BeautifulSoup(response.content, features="html.parser")
            sun_azimuth = soup.find(id='sunaz').get_text()
            sun_altitude = soup.find(id='sunalt').get_text()
            return sun_azimuth, sun_altitude

        except Exception as error:
            LOGGER.error(f'An error has occurred: {error}')
            return None

    def get_openuv_info(self, city):
        """
        Fetches UV information from api.openuv.io
        Information includes uv index, ozone level, safe exposure time etc...
        Updates the Instance Variable self.uv_info which is a dictionary
        :param city:    string. Name of a city which appears in 'locations.py' file for example: London, Tirana, etc
        :return:        True
                        False
        """
        latitude = locations.locations[city]['Latitude']
        longitude = locations.locations[city]['Longitude']
        try:
            url = f'http://api.openuv.io/api/v1/uv?lat={latitude}&lng={longitude}'
            LOGGER.info(f'Fetching UV index values from: {url}')
            payload = {app_config.OPENUV_HEADER: app_config.OPENUV_TOKEN}
            response = requests.get(url, verify=False, headers=payload)
            LOGGER.debug(f'Got response: {response.content}')
            self.uv_info = response.json()
            return True

        except Exception as error:
            LOGGER.error(f'An error has occurred: {error}')
            return False

    def parse_openuv_json(self):
        """
        Parsing the content of self.uv_info (which is the returned json from api.openuv.io)
        and updates instance variables.
        :return:        True
                        False
        """
        try:
            self.uv_index = self.uv_info['result']['uv']
            self.ozone_level = self.uv_info['result']['ozone']
            self.safe_exposure_time = self.uv_info['result']['safe_exposure_time']
            # self.set1 = self.safe_exposure_time['st1']
            # print(self.set1)
            self.sun_azimuth_openuv = self.uv_info['result']['sun_info']['sun_position']['azimuth']
            self.sun_altitude_openuv = self.uv_info['result']['sun_info']['sun_position']['altitude'] * Data.radian
            return True

        except Exception as error:
            LOGGER.error(f'An error has occurred: {error}')
            return False

    def fetch_clouds_info(self, city):
        """
        fetching cloud coverage from: api.solcast.com
        :param city:    string. Name of a city which appears in 'locations.py' file for example: London, Tirana, etc
        :return:        True
                        False
        """
        latitude = locations.locations[city]['Latitude']
        longitude = locations.locations[city]['Longitude']
        api_key = app_config.SOLCAST_API_KEY
        try:
            url = f'{app_config.SOLCAST_URL}latitude={latitude}&longitude={longitude}&api_key={api_key}&format=json'
            LOGGER.info(f'Fetching clouds information from: {url}')
            response = requests.get(url, verify=False)
            LOGGER.debug(f'Got response: {response.content}')
            self.clouds_info = response.json()
            self.cloud_opacity = self.clouds_info['forecasts'][0]['cloud_opacity']
            return True

        except Exception as error:
            LOGGER.error(f'An error has occurred: {error}')
            return False

    def fetch_accuweather_info(self, city):
        """
        Web scraping from www.accuweather.com/en/
        :param city:    string. Name of a city which appears in 'locations' dictionary for example: London, Tirana, etc
        :return:        True
                        False
        :update:        self.cloud_cover
                        self.cloud_ceiling
                        self.precipitation
                        self.sky
        """
        try:
            uri = locations.locations[city]['uri']
            url = f'{app_config.ACCUWAETHER_URL}{uri}'
            LOGGER.info(f'Fetching clouds info from: {url}')
            headers = {'user-agent': app_config.CHROME_USER_AGENT}
            response = requests.get(url, headers=headers, verify=False)

            soup = BeautifulSoup(response.content, features="html.parser")
            for element in soup.find_all('div', class_='detail-item spaced-content'):
                if re.findall('Cloud Cover', element.text):
                    full_cell_text = element.text
                    text_splitted_list = full_cell_text.split(' ')
                    value = text_splitted_list[1].split('\n')
                    self.cloud_cover = value[1]
                if re.findall('Cloud Ceiling', element.text):
                    full_cell_text = element.text
                    text_splitted_list = full_cell_text.split(' ')
                    value = text_splitted_list[1].split('\n')
                    self.cloud_ceiling = value[1]
                if re.findall('Precipitation', element.text):
                    full_cell_text = element.text
                    text_splitted_list = full_cell_text.split(' ')
                    value = text_splitted_list[1].split('\n')
                    self.precipitation = value[1]

            element = soup.find_all('div', class_='phrase')
            self.sky = element[0].text
            return True

        except Exception as error:
            LOGGER.error(f'An error has occurred: {error}')
            return False


if __name__ == '__main__':
    location = 'Stockholm'
    data = Data()
    data.get_openuv_info(location)
    data.parse_openuv_json()


