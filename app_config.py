import os
import csv
import datetime


timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d__UTC%H-%M-%S')

OPENUV_HEADER = 'x-access-token'
OPENUV_TOKEN = '92096e5152c61f0d3f5c64a3e89fa55e'

SOLCAST_API_KEY = 'fJxPhN60I9rweds-KkfikmCHlYdNdgSI'
SOLCAST_URL = f'https://api.solcast.com.au/radiation/forecasts?'

ACCUWAETHER_URL = 'https://www.accuweather.com/en/'
CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

CSV_DIR_NAME = 'csv_files'
CSV_FILE_NAME = 'data.csv'
CSV_HEADERS_LIST = ['UTC Timestamp', 'City', 'Country', 'Latitude', 'Longitude', 'UV Index', 'Ozone level',
                    'SET1', 'SET2', 'SET3', 'SET4', 'SET5', 'SET6', 'Sun Azimuth', 'Sun Altitude', 'Cloud Ceiling',
                    'Cloud Cover', 'Sky', 'Precipitation ', 'Cloud opacity']

if not os.path.exists(CSV_DIR_NAME):
    os.makedirs(CSV_DIR_NAME)

if not os.path.exists(os.path.join(CSV_DIR_NAME, CSV_FILE_NAME)):
    with open(os.path.join(CSV_DIR_NAME, CSV_FILE_NAME), 'a', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        csv_writer.writerow(CSV_HEADERS_LIST)

LOGS_DIR_NAME = 'Logging'
LOG_FILE_NAME = f'log__{timestamp}.log'
LOG_FILE_MODE = 'w'  # a = append , w = overwrite
LOG_FILE_PATH = os.path.join(LOGS_DIR_NAME, LOG_FILE_NAME)

if not os.path.exists(LOGS_DIR_NAME):
    os.makedirs(LOGS_DIR_NAME, exist_ok=True)


