import weather_info as winfo
import locations
import logging
import datetime
import logger
import csv
import app_config
import os


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logger.LOG_LEVEL)


parameters_list = list()
path_to_csv_file = os.path.join(app_config.CSV_DIR_NAME, app_config.CSV_FILE_NAME)
data = winfo.Data()

for city in locations.locations:
    parameters_list.clear()
    LOGGER.info(f'New cycle for location: {city}')

    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d  UTC%H:%M:%S')
    parameters_list.append(current_time)
    parameters_list.append(city)
    parameters_list.append(locations.locations[city]['Country'])
    parameters_list.append(locations.locations[city]['Latitude'])
    parameters_list.append(locations.locations[city]['Longitude'])

    data.get_openuv_info(city)
    data.parse_openuv_json()
    parameters_list.append(data.uv_index)
    parameters_list.append(data.ozone_level)
    parameters_list.append(data.safe_exposure_time['st1'])
    parameters_list.append(data.safe_exposure_time['st2'])
    parameters_list.append(data.safe_exposure_time['st3'])
    parameters_list.append(data.safe_exposure_time['st4'])
    parameters_list.append(data.safe_exposure_time['st5'])
    parameters_list.append(data.safe_exposure_time['st6'])
    parameters_list.append(f'{data.sun_azimuth_openuv:.5f}')
    parameters_list.append(f'{data.sun_altitude_openuv:.3f}')

    data.fetch_accuweather_info(city)
    parameters_list.append(data.cloud_ceiling)
    parameters_list.append(data.cloud_cover)
    parameters_list.append(data.sky)
    parameters_list.append(data.precipitation)

    data.fetch_clouds_info(city)
    parameters_list.append(data.cloud_opacity)

    with open(path_to_csv_file, 'a', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        csv_writer.writerow(parameters_list)
