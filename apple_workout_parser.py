#!/usr/bin/python3
import sys

from lxml import etree

import command_line
import logging
import constants
from dateutil.parser import parse

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def init_logging():
    if constants.DEBUG:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)


def add_stat(stat_year, stat_month, stat_day, stat_distance, stat_unit, workout_stats):
    if stat_year not in workout_stats.keys():
        workout_stats[stat_year] = {}

    if stat_month not in workout_stats[stat_year].keys():
        workout_stats[stat_year][stat_month] = []

    distance = stat_distance
    if stat_unit == "km":
        distance *= 0.621371
    elif stat_unit != "mi":
        raise NotImplementedError("I only support miles or kilometers!")

    workout_stats[stat_year][stat_month].append((stat_day, distance))


def print_year_stats(yearly_stats, this_year):
    print(f"Summary for year {this_year}")
    year_stats = yearly_stats[this_year]
    yearly_total = 0
    for i in range(1, 13):
        if i in year_stats.keys():
            monthly_total = round(sum(distance for d, distance, in year_stats[i]), 2)
            yearly_total += monthly_total
            print(f"    {months[i]}: {monthly_total}")
    print(f"Total for year: {yearly_total}")


def print_month_stats(this_year, this_month, stats_for_month):
    print(f"Stats for month of {months[this_month]}, {this_year}")
    for stat in stats_for_month:
        d, distance = stat
        print(f"    {months[this_month]} {d}: {str(round(distance, 2))}mi")
    print(
        f"Total for {months[this_month]}: {round(sum(distance for d, distance in stats_for_month), 2)}mi"
    )


def print_stats(yearly_stats, this_year, this_month):
    if this_month is not None:
        print_month_stats(this_year, this_month, yearly_stats[this_year][this_month])
    else:
        print_year_stats(yearly_stats, this_year)


workout_types = {
    "W": constants.apple_workout_activity_type_value_walk,
    "R": constants.apple_workout_activity_type_value_run,
}


def is_desired_workout_type(workout_element, workout_type_key):
    return (
        workout_element.get(constants.apple_workout_activity_type_key)
        == workout_types[workout_type_key]
    )


def is_workout_distance(element):
    return (
        element.tag == constants.apple_workout_stats_tag
        and element.get(constants.apple_stat_type_key)
        == constants.apple_workout_distance_value
    )


def get_workout_distance_element(workout_element):
    for child_element in workout_element:
        if is_workout_distance(child_element):
            return child_element


if __name__ == "__main__":
    init_logging()
    file, workout_type, year, month = command_line.parse_command_line()

    stats = {}
    for event, workout in etree.iterparse(file, tag=constants.apple_workout_tag):
        if is_desired_workout_type(workout, workout_type):
            child = get_workout_distance_element(workout)
            start_date = parse(child.get(constants.apple_stat_start_date_key))
            if year == start_date.year:
                add_stat(
                    year,
                    start_date.month,
                    start_date.day,
                    float(child.get(constants.apple_stat_sum_key)),
                    child.get(constants.apple_stat_unit_key),
                    stats,
                )
                logging.debug(
                    f"Found workout: {workout.get(constants.apple_workout_activity_type_key)}, "
                    + f"time={str(start_date)}, distance={child.get(constants.apple_stat_sum_key)}"
                    + f"{child.get(constants.apple_stat_unit_key)}"
                )
    print_stats(stats, year, month)
