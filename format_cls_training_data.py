"""
Take cleaned recipe data, and format it into a TSV that works with Uber PPLM
to train a classifier for various recipe tags.

Format: TSV with structure: class \t text

Output:
vegan.tsv
"""

import json
import csv

# Available tags:
# AllRecipes:  'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# BBCGoodFood: 'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Chowhound:   'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Commoncrawl: 'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Food.com:    'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Food52:      'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# FoodNetwork: 'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Showme:      'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# SimplyRec:   'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'
# Smitten:     'Vegetarian', 'Vegan', 'Healthy', 'Gluten-free'

# Read in all recipe question and answer data
data_path = '/alhegel/scrapes/'
sources = ['allrecipes_clean.jl', 'bbcgoodfood_clean.jl', 'chowhound_clean.jl',
           'commoncrawl_recipes_dataset_clean.jl', 'food_clean.jl', 'food52_clean.jl',
           'food52comment_clean.jl', 'foodnetwork_clean.jl', 'showmetheyummy_clean.jl',
           'simplyrecipes_clean.jl', 'smittenkitchen_clean.jl']
output_path = '/alhegel/gitrepos/PPLM/'

data = []
for data_source in sources:
    class1 = 0
    class0 = 0
    with open(data_path + data_source, 'r') as infile:
        for line in infile:
            line = json.loads(line)
            newline = []

            if 'tags' in line['recipe_schema']:
                if 'Vegan' in line['recipe_schema']['tags']:
                    newline.append('vegan')
                    class1 += 1
                else:
                    newline.append('non_vegan')
                    class0 += 1

            title = line['recipe_schema']['name']
            ingredients = ' '.join(line['recipe_schema']['recipeIngredient'])
            instructions = ' '.join(line['recipe_schema']['recipeInstructions'])
            try:
                text = title + ' ' + ingredients + ' ' + instructions
            except:
                print(line)
                exit()

            # truncate but not in the middle of a word
            max_length = 1000  # PPLM code has 100
            if len(text) > max_length:
                text = ' '.join(text[:max_length+1].split(' ')[0:-1])

            newline.append(text)

            data.append(newline)
    print(data_source)
    print('vegan', str(class1))
    print('non_vegan', str(class0))
    print()
print(len(data))

# Output files
with open(output_path + 'vegan.tsv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    for row in data:
        writer.writerow(row)
