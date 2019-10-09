from __future__ import division
from __future__ import print_function

import csv

import pandas as pd
import cea.config
import cea.inputlocator
import cea

__author__ = "Jimeno Fonseca"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

COLUMNS_SCHEDULES = ['DAY',
                     'HOUR',
                     'OCCUPANCY',
                     'APPLIANCES_LIGHTING',
                     'DOMESTIC_HOT_WATER',
                     'SETPOINT_HEATING',
                     'SETPOINT_COOLING',
                     'PROCESSES']

DAY = ['WEEKDAY'] * 24 + ['SATURDAY'] * 24 + ['SUNDAY'] * 24
HOUR = range(1, 25) + range(1, 25) + range(1, 25)


def read_cea_schedule(path_to_cea_schedule):
    '''
    reader of schedule file
    .ceaschedule
    :param path:
    :return:
    '''

    with open(path_to_cea_schedule) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                metadata = row[1]
            elif i == 1:
                monthly_multiplier = [round(float(x), 2) for x in row[1:]]

    schedule_data = pd.read_csv(path_to_cea_schedule, skiprows=2).T
    schedule_data = dict(zip(schedule_data.index, schedule_data.values))
    schedule_complementray_data = {'METADATA': metadata, 'MONTHLY_MULTIPLIER': monthly_multiplier}
    schedule_data.update(schedule_complementray_data)
    return schedule_data


def save_cea_schedule(schedule_data, path_to_building_schedule):

    # unpack variables
    metadata = schedule_data['metadata']
    monthly_multiplier = schedule_data['monthly_multiplier']
    occupancy_weekday = schedule_data['occupancy_weekday']
    occupancy_saturday = schedule_data['occupancy_saturday']
    occupancy_sunday = schedule_data['occupancy_sunday']
    appliances_weekday = schedule_data['appliances_weekday']
    appliances_saturday = schedule_data['appliances_saturday']
    appliances_sunday = schedule_data['appliances_sunday']
    domestic_hot_water_weekday = schedule_data['domestic_hot_water_weekday']
    domestic_hot_water_saturday = schedule_data['domestic_hot_water_saturday']
    domestic_hot_water_sunday = schedule_data['domestic_hot_water_sunday']
    setpoint_heating_weekday = schedule_data['setpoint_heating_weekday']
    setpoint_heating_saturday = schedule_data['setpoint_heating_saturday']
    setpoint_heating_sunday = schedule_data['setpoint_heating_sunday']
    setpoint_cooling_weekday = schedule_data['setpoint_cooling_weekday']
    setpoint_cooling_saturday = schedule_data['setpoint_cooling_saturday']
    setpoint_cooling_sunday = schedule_data['setpoint_cooling_sunday']
    processes_weekday = schedule_data['processes_weekday']
    processes_saturday = schedule_data['processes_saturday']
    processes_sunday = schedule_data['processes_sunday']

    #local variables
    occupancy_72h = []
    appliances_72h = []
    domestic_hot_water_72h = []
    setpoint_heating_72h = []
    setpoint_cooling_72h = []
    processes_72h = []

    occupancy_72h.append(occupancy_weekday)
    occupancy_72h.append(occupancy_saturday)
    occupancy_72h.append(occupancy_sunday)

    appliances_72h.append(appliances_weekday)
    appliances_72h.append(appliances_saturday)
    appliances_72h.append(appliances_sunday)

    domestic_hot_water_72h.append(domestic_hot_water_weekday)
    domestic_hot_water_72h.append(domestic_hot_water_saturday)
    domestic_hot_water_72h.append(domestic_hot_water_sunday)

    setpoint_heating_72h.append(setpoint_heating_weekday)
    setpoint_heating_72h.append(setpoint_heating_saturday)
    setpoint_heating_72h.append(setpoint_heating_sunday)

    setpoint_cooling_72h.append(setpoint_cooling_weekday)
    setpoint_cooling_72h.append(setpoint_cooling_saturday)
    setpoint_cooling_72h.append(setpoint_cooling_sunday)

    processes_72h.append(processes_weekday)
    processes_72h.append(processes_saturday)
    processes_72h.append(processes_sunday)

    METADATA = ['METADATA', str(metadata)]
    MULTIPLIER = ['MONTHLY_MULTIPLIER'] + [str(round(float(x), 2)) for x in monthly_multiplier]

    PROFILE = [DAY, HOUR, occupancy_72h, appliances_72h, domestic_hot_water_72h, setpoint_heating_72h,
               setpoint_cooling_72h, processes_72h]
    PROFILE_NEW = map(list, zip(*PROFILE))

    with open(path_to_building_schedule, "wb") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(METADATA)
        csvwriter.writerow(MULTIPLIER)
        csvwriter.writerow(COLUMNS_SCHEDULES)
        for row in PROFILE_NEW:
            csvwriter.writerow(row)

def main(config):
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    path_database = locator.get_database_standard_schedules('CH-SIA-2014')
    path_to_building_schedule = locator.get_database_standard_schedules_use(path_database, 'MULTI_RES')
    read_cea_schedule(path_to_building_schedule)

if __name__ == '__main__':
    main(cea.config.Configuration())
