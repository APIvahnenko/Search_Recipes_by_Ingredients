from Database import *
from VariableByteEncoder import *

database = Database("recipes")
database.AddToIngredientIndexTable("olive oil", 100)
database.AddToIngredientIndexTable("chicken",   100)
database.AddToIngredientIndexTable("spinach",   100)
database.AddToIngredientIndexTable("fish",      200)
database.AddToIngredientIndexTable("chicken",   200)
database.AddToIngredientIndexTable("chicken",   300)
database.AddToIngredientIndexTable("spinach",   300)

recipeIds = database.GetRecipeIds("olive oil")
print(recipeIds)
recipeIds = database.GetRecipeIds("chicken")
print(recipeIds)
recipeIds = database.GetRecipeIds("spinach")
print(recipeIds)
recipeIds = database.GetRecipeIds("fish")
print(recipeIds)