#!/usr/bin/env python3

import pymysql
from VariableByteEncoder import *

class Database:
    database = None
    cursor   = None
    
    def __init__(self, databaseName):
        self.database = pymysql.connect("localhost", "root", "", databaseName)
        self.cursor   = self.database.cursor()
        self.CreateIngredientIndexTable()
        self.CreateRecipeInfoTable()
    
    def __del__(self):
        self.database.close()
    
    def CreateIngredientIndexTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS ingredient_index")
        self.cursor.execute("""CREATE TABLE ingredient_index (
                               ingredient             VARCHAR(255),
                               recipe_ids             BLOB,
                               ingredient_synonyms    VARCHAR(255),
                               ingredient_temperature VARCHAR(255))""")
    
    # def CreateIngredientIndexTable(self):
    #     self.cursor.execute("DROP TABLE IF EXISTS ingredient_index")
    #     self.cursor.execute("""CREATE TABLE ingredient_index (
    #                            ingredient             VARCHAR(255),
    #                            recipe_ids             VARCHAR(10000),
    #                            ingredient_synonyms    VARCHAR(255),
    #                            ingredient_temperature VARCHAR(255))""")
    
    def CreateRecipeInfoTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS recipe_info")
        self.cursor.execute("""CREATE TABLE recipe_info (
                               recipe_id        MEDIUMINT UNSIGNED,    
                               recipe_url       VARCHAR(1000),    
                               image_url        VARCHAR(1000),    
                               title            VARCHAR(1000),    
                               description      VARCHAR(10000),    
                               preparation_time MEDIUMINT UNSIGNED,            
                               cook_time        MEDIUMINT UNSIGNED,            
                               serving_count    MEDIUMINT UNSIGNED,
                               ingredient_count TINYINT UNSIGNED)""")
    
    def AddToIngredientIndexTable(self, ingredient, recipeId):
        recipeIds = []
        
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # If it is a new ingredient.
            recipeIds.append(recipeId)
            self.cursor.execute("INSERT INTO ingredient_index\
                                 (ingredient, recipe_ids)    \
                                 VALUES (%s, %s)", (ingredient, encode(recipeIds)))
        else:
            self.cursor.execute("SELECT recipe_ids    \
                                 FROM ingredient_index\
                                 WHERE ingredient = %s", ingredient)
            recipeIds = decode(self.cursor.fetchone()[0])
            recipeIds.append(recipeId)
            self.cursor.execute("UPDATE ingredient_index\
                                 SET recipe_ids = %s    \
                                 WHERE ingredient = %s", (encode(recipeIds), ingredient))
        
        self.database.commit()
    
    # def AddToIngredientIndexTable(self, ingredient, recipeId):    
    #     self.cursor.execute("SELECT count(*)      \
    #                          FROM ingredient_index\
    #                          WHERE ingredient = %s", ingredient)
    # 
    #     if self.cursor.fetchone()[0] == 0:    # If it is a new ingredient.    
    #         recipeIdsString = ','.join(recipeIds)
    #         self.cursor.execute("INSERT INTO ingredient_index\
    #                              (ingredient, recipe_ids)    \
    #                              VALUES (%s, %s)", (ingredient, str(recipeId)))
    #     else:
    #         self.cursor.execute("SELECT recipe_ids    \
    #                              FROM ingredient_index\
    #                              WHERE ingredient = %s", ingredient)
    #         recipeIds = self.cursor.fetchone()[0]
    #         recipeIds = recipesIds + "," + str(recipeId)
    #         self.cursor.execute("UPDATE ingredient_index\
    #                              SET recipe_ids = %s    \
    #                              WHERE ingredient = %s", (recipeIds, ingredient))
    # 
    #     self.database.commit()
    
    
    
    
    
    
    
    #def AddIngredientSynonymsToIngredientIndexTable(self, ingredient, ingredientSynonyms):
    #def GetIngredientSynonyms(self, ingredient):
    #def GetExtendedRecipeIds(self, ingredients):
    #def AddIngredientTemperatureToIngredientIndexTable(self, ingredient, ingredientTemperature):
    #def GetIngredientTemperature(self, ingredientTemperature): 
    
    
    
    
    def AddToRecipeInfoTable(self, recipeId, recipeUrl, imageUrl, title, description,
                             preparationTime, cookTime, servingCount, ingredientCount):
        self.cursor.execute("""INSERT INTO recipe_info
                               (recipe_id, recipe_url, image_url, title, description,
                                preparation_time, cook_time, serving_count, ingredient_count)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                      (recipeId, recipeUrl, imageUrl, title, description,
                                       preparationTime, cookTime, servingCount, ingredientCount))
        self.database.commit()
    
    def GetRecipeIds(self, ingredient):
        self.cursor.execute("SELECT recipe_ids    \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        return decode(self.cursor.fetchone()[0])
        # return self.cursor.fetchone()[0] 