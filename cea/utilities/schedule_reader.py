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

    return schedule_data, schedule_complementray_data


def save_cea_schedule(schedule_data, schedule_complementray_data, path_to_building_schedule):



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
