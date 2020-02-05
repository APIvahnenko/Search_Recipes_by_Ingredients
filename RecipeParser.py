#!/usr/bin/env python3

import re
from nltk.stem import PorterStemmer
from Database import *

class RecipeParser:
    recipeFile       = "content.txt"
    recipeFileHandle = None
    database         = None
    ps               = None
    
    def __init__(self):
        self.recipeFileHandle = open(self.recipeFile, 'r', encoding = "utf-8")
        self.database         = Database("recipes")
        self.ps               = PorterStemmer()
    
    def __del__(self):
        self.recipeFileHandle.close()
    
    def cleaning_ing_list(self, ingredients):
        #getting a list of stop phrases
        stop_phrases = [stop_words.rstrip('\n') for stop_words in open("recipe_stopwords.txt", 'r', encoding = "utf-16")]
        final_list   = []
        
        for ing in ingredients:
            #removing text in brackets
            ing = re.sub("\s?[\(\[].*?[\)\]]", "", ing)
            
            #removing anything extra in the ingredient discription (after ',')
            if "," in ing:
                clean_ing, extra = ing.split(',', 1)
                ing = clean_ing
            
            #ing only words
            pattern = re.compile(r"\b[a-zA-Z-]+\b")
            ing_words = pattern.findall(ing)
            
            #removing stopwords
            filtered_ing = [w for w in ing_words if w not in stop_phrases]
            
            #stemming
            clean_ing = []
            for word in filtered_ing:
                clean_ing.append(self.ps.stem(word))
            
            #lower caseing & appending
            if len(clean_ing) > 0:
                list_of_ing.append(' '.join(clean_ing).lower())
        
        final_list = []
        final_set = set(list_of_ing)
        for item in final_set:
            final_list.append(item)
            
        return final_list
    
    def clean_time(self, string):
        h_match  = re.findall(r"([0-9]+\s?[h]+)", string, re.I)
        m_match  = re.findall(r"([0-9]+\s?[m]+)", string, re.I)
        to_match = re.findall(r"([0-9]+\s[t][o]\s+[0-9])", string, re.I) #eg. "1 to 2 hours"
        
        hours   = 0
        minutes = 0
        
        #key phrase search
        if "to" in string:
            if to_match:
                string = string.split("to")[1]
            else:
                string = string.split("to")[0]

        #if contains hours
        if h_match:
            hours = int(re.findall(r'\d+', str(h_match))[0])
                
        #if contains min
        if m_match:
            minutes = int(re.findall(r'\d+', str(m_match))[0])
            
        #if does not contains min or hours
        if not h_match and not m_match:
            if "overnight" in string:
                hours = 8
            else:
                print("time input error: ", string)
        else:
            return hours*60 + minutes
    
    def ParseRecipeFile(self):
        line_num    = 1
        ing_num     = 0
        recipe_id   = 0
        ingredients = []
        description = ""
        
        for line in self.recipeFileHandle.readlines():
            if line_num == 1:
                url = line
                #print("URL: ", url)
                recipe_id += 1
                line_num  += 1
                continue
        
            if line_num == 2:
                img_url = line
                #print("image URL: ", img_url)
                line_num += 1
                continue
        
            if line_num == 3:
                title = line
                #print("recipe title: ", title)
                line_num += 1
                continue
                
            if line_num == 4:
                if "preptime" in line:
                    #printing discription in a single line
                    #print("discription: ", re.sub("\n", "", description))
                    line_num += 1
                    continue
                else:
                    description = description + " " + line
                    continue
            
            if line_num == 5:
                prep_time = self.clean_time(line)
                #print("\nprep time: ", prep_time, " min.\n")
                line_num += 1
                continue
                
            if line_num == 6:
                cook_time = self.clean_time(line)
                #print("cook time: ", cook_time, " min.\n")
                line_num += 1
                continue
            
            if line_num == 7:
                try:
                    servings = int(re.findall(r'\d+',line)[0])
                except:
                    servings = 1 #e.g. "Makes one jar"
                    
                #print("servings: ", servings, "\n")
                line_num += 1
                continue
        
            if "*****eol*****" in line:
                clean_ingredients = self.cleaning_ing_list(ingredients)
                
                #print("ingredients: ", clean_ingredients)
                #print("\nnum of ingredients: ", ing_num)
                #print("-----")
                
                for ingredient in clean_ingredients:
                    self.database.AddToIngredientIndexTable(ingredient, recipe_id)
                
                self.database.AddToRecipeInfoTable(recipe_id, url, img_url, title, description,
                                                   prep_time, cook_time, servings, len(clean_ingredients))
                
                line_num    = 1
                ing_num     = 0
                ingredients = []
                description = ""
                
                continue
            
            if line_num > 7:
                #print(line)

                #words of an ingridient entry
                line_words = line.split()

                #key words search
                if "and" in line_words:
                    primary_ing, extra_ing = line.split("and", 1)
                    ingredients.extend([primary_ing, extra_ing])
                    ing_num += 1 #count extra ing
                
                elif "and/or" in line_words:
                    primary_ing, alt_ing = line.split("and/or", 1)
                    ingredients.extend([primary_ing, alt_ing])
                    #not counting alternative ingridient
                
                elif "plus extra" in line:
                    primary_ing, extra_same = line.split("plus extra", 1)
                    ingredients.append(primary_ing) 
                    #excluding since the same ingridient is used

                elif "plus" in line_words:
                    primary_ing, extra_ing = line.split("plus", 1)
                    ingredients.extend([primary_ing, extra_ing])
                    ing_num += 1 #count extra ing
                
                #dure to the similarity in spelling for and or are special case
                elif "or" in line_words:
                    
                    #looking at the possitions of word in line
                    if "for" in line_words:
                        pos_for = line.find("for")
                        pos_or  = line.find("or", 1)
                        
                        if pos_for > pos_or:
                            primary_ing, alternative = line.split("or", 1)
                            alt_ing, why_needed      = alternative.split("for", 1)
                            ingredients.extend([primary_ing, alt_ing])
                            #not counting alternative ingridient
                    
                        else:
                            primary_ing, why_needed = line.split("for", 1)
                            ingredients.append(primary_ing) 
                            #excluding why ingredient is needed
                        
                    else:
                        primary_ing, alt_ing = line.split("or", 1)
                        ingredients.extend([primary_ing, alt_ing])
                        #not counting alternative ingridient

                else:
                    ingredients.append(line)
                
                ing_num  += 1
                line_num += 1
                continue

            else:
                print("error")