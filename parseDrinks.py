#!env python
import json
import re
from pprint import pprint


class Drink:
    def __init__(self, drink_name):
        self.instructions = []
        self.drink_name = drink_name

    def add_to_instructions(self, text):
        self.instructions.append(text)

    def get_instructions(self):
        return self.instructions

    def get_drink_name(self):
        return self.drink_name


measurements = ['tsp', 'dash', 'oz', 'ounce']
drink = None
drinks = {}
with open('Classics.txt', 'r', encoding='UTF-8') as classics:
    for line in classics:
        if not drink:
            drink = Drink(line.rstrip('\n'))
        elif not line.strip():
            drinks[drink.get_drink_name()] = {"Instructions": drink.get_instructions()}
            drink = None
        elif "Ingredients" not in line:
            matches = re.match('(\d+ */* */*\d*/*\d*) ((tsp|dash|oz|ounce)*(es|s)* )*(.*)', line.rstrip('\n'))
            if matches:
                drink.add_to_instructions({"Quantity": matches.group(1),
                                           "Unit": (matches.group(3) or "") + (matches.group(4) or ""),
                                           "Liquor": matches.group(5)})
            else:
                drink.add_to_instructions(line.rstrip('\n'))

drink = None
show = None
show_date = None
last_line = None
with open('GregsDrinks.txt', 'r', encoding='UTF-8') as classics:
    for line in classics:
        if last_line == line:
            if drink:
                drinks[drink.get_drink_name()] = {"Show": show,
                                                  "Show Date": show_date,
                                                  "Instructions": drink.get_instructions()}
            show = None
            show_date = None
            drink = None
        elif not line.strip():
            if drink:
                drinks[drink.get_drink_name()] = {"Show": show,
                                                  "Show Date": show_date,
                                                  "Instructions": drink.get_instructions()}
            drink = None
            instructions = []
        elif not show:
            show = line.rstrip('\n')
        elif not show_date:
            show_date = line.rstrip('\n')
        elif not drink and line.rstrip('\n'):
            drink = Drink("Greg {}".format(line.rstrip('\n')))
        else:
            matches = \
                re.match("( )*(•|-)*(\.*\d*.*\d+[a-zA-Z]* (([tT]sp|[dD]ash|[oO]z|[oO]unce|[mM][lL]|[pP]art)*(es|s)*(\.)*){1} )(.+)", line.rstrip('\n'))
            if matches:
                pprint(matches.groups())
                quantity_and_unit = (matches.group(3) or "").split("or")[0].replace("-", "").strip()
                try:
                    unit = quantity_and_unit.split(' ')[1]
                except IndexError:
                    unit = None
                drink.add_to_instructions({"Quantity": quantity_and_unit.split(' ')[0],
                                           "Unit": (unit or matches.group(4)).strip(),
                                           "Liquor": matches.group(8).replace("of", "").strip()})
            else:
                drink.add_to_instructions(line.replace("-", "").strip().strip('\n'))
        last_line = line

with open('Drinks.json', 'w') as drink_out:
    drink_out.write(json.dumps(drinks, indent=4))
