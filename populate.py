from msilib.schema import Error
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecipApp.settings')
import django
django.setup()
import requests
from main.models import Ingredient, Recipe

url = 'https://api.spoonacular.com/recipes/716429/information?includeNutrition=false'

headers = {
	"X-RapidAPI-Key": "0aa8b2c149564b51ad1750abc23a1b9a",
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

import random
recipe_ids = set()
def populate_recipe(n):
	'''creates ids to add to the database and a set of the added ids'''
	for new in range(n):
		id = random.randint(1, 40000)		
		if id in recipe_ids:
			continue	
		else: recipe_ids.add(id)		

		response_instruction = requests.get(f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey=0aa8b2c149564b51ad1750abc23a1b9a')
		response_recipe = requests.get(f'https://api.spoonacular.com/recipes/{id}//information?apiKey=0aa8b2c149564b51ad1750abc23a1b9a&includeNutrition=true')
		
		if response_instruction.status_code != 200 or response_recipe.status_code != 200:
			print(response_instruction)
			print(response_recipe)
			continue

		data_instructions = response_instruction.json()
		data_recipe = response_recipe.json()
		
		instructions = []
		for instruction in data_instructions:	
			for step in instruction['steps']:
				instructions.append((step['number'], step['step']))
		
		recipe_inst = Recipe()

		ingredients = data_recipe['extendedIngredients']	

		recipe_inst.title = data_recipe['title']
		recipe_inst.image = data_recipe['image']
		recipe_inst.description = data_recipe['summary']
		recipe_inst.instructions = instructions
		recipe_inst.servings = data_recipe['servings']
		recipe_inst.prep_time = data_recipe['readyInMinutes']
		recipe_inst.gluten_free = data_recipe['glutenFree'] 
		recipe_inst.vegan = data_recipe['vegan'] 
		recipe_inst.veggie = data_recipe['vegetarian'] 
		recipe_inst.very_healthy = data_recipe['veryHealthy']     
		recipe_inst.type = data_recipe['dishTypes'] 
		recipe_inst.cusine = data_recipe['cuisines']  
		recipe_inst.occasion = data_recipe['occasions']
		print(recipe_inst)

		recipe_inst.save() 		

		for ingredient in ingredients:
			name = ingredient['name']
			unit = ingredient['unit']
			amount = ingredient['amount']
			ingredient = Ingredient.objects.get_or_create(name = name, unit = unit, amount = amount)
			recipe_inst.ingredients.add(ingredient[0])	

# populate_recipe(200)
print(recipe_ids)	

