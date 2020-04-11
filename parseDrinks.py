import json
import re
from pprint import pprint

drinks = {}
drink = None
ingredients = []
with open('Classics.txt', 'r', encoding='UTF-8') as classics:
    for line in classics:
        if not drink:
            drink = line.rstrip('\n')
        elif not line.strip():
            drinks[drink] = ingredients
            drink = None
            ingredients = []
        elif "Ingredients" not in line:
            #matches = re.match('(\d+ */* */*\d*)(.*)', line.rstrip('\n'))
            ingredients.append(line.rstrip('\n'))

#Nikki's new favorite
#Apr 10, 2020
#
#Division Bell
#1 oz Mezcal
#3/4 oz Aperol
#3/4 oz Lime Juice
#1/2 oz Maraschino Liqueur
#Garnish with Grapefruit twist
#
#
#
#drink = None
#ingredients = []
#with open('GregsDrinks.txt', 'r', encoding='UTF-8') as gregs:
#    for line in gregs:
#        if not drink:
#            drink = line
            
#pprint(drinks)

with open('Drinks.json', 'w') as drink_out:
    drink_out.write(json.dumps(drinks, indent=4))