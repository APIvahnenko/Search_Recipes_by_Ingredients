import pymysql
import re
import time
from VariableByteEncoder import *
import json
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app,resources={r'/*': {'origins': '*'}})

def getlocation(ip):
    import pygeoip
    dataname = pygeoip.GeoIP(r'C:\Users\mraja\Downloads\Programs\GeoLiteCity.dat')
    data = dataname.record_by_name(ip)
    country = data['country_name']
    city = data['city']
    longi = data['longitude']
    lat = data['latitude']
    return str(city),str(country),str(lat),str(longi)



#for getting ip
def getip():
    import json
    from urllib import request
    url = 'http://ipinfo.io/json'
    response = request.urlopen(url)
    str_response = response.read().decode('utf-8')
    data1 = json.loads(str_response)
    IP=data1['ip']
    region = data1['region']
    return IP,region



@app.route("/test")
def test():
    args = request.args
    #return json.dumps({'data':"gotit "+str(args['city'])})
    start = time.time()
    # Open database connection
    db = pymysql.connect("localhost","root","","recipes" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    print(args)
    ip,region = getip()
    print(region,getlocation(ip))
    if args['city'].lower() == 'hi':
        import sys
        #query = ' '.join(sys.argv[1:])
        query = "beef"
        query = re.split(r'[, - : ; + ! @ # $ ^ & * . " \' { } | \s+ ]+',query.strip())

        recipe_dict = dict()
        for word in query:
            #word = PorterStemmer().stem(word)
            sql = ("""SELECT recipe_ids FROM ingredient_index WHERE ingredient LIKE %s""", "%"+word+"%")
            cursor.execute(*sql)
            results = cursor.fetchall()
            if len(results)==0:
                #sys.exit(1)
                continue
            for row in results:
                recipe_id_list = decode(row[0])
                for recipe_id in recipe_id_list:
                    if recipe_id not in recipe_dict:
                        recipe_dict[recipe_id] = 1
                    else:
                        recipe_dict[recipe_id] +=1
        recipe_common_ing_count = {}
        for recipe in recipe_dict.keys():
            if recipe_dict[recipe] > 1:
                sql = ("""SELECT ingredient_count FROM recipe_info WHERE recipe_id LIKE %s""", recipe)
                cursor.execute(*sql)
                recipe_common_ing_count[recipe] = int(cursor.fetchone()[0])-recipe_dict[recipe]

        checkbox = "oil,water"
        checkbox_ing = checkbox.strip().split(",")

        for ing in checkbox_ing:
            if ing !="":
                #ing = PorterStemmer().stem(ing)
                sql = ("""SELECT recipe_ids FROM ingredient_index WHERE ingredient LIKE %s""", word)
                cursor.execute(*sql)
                results = cursor.fetchall()
                if len(results)==0:
                    continue
                for row in results:
                    recipe_id_list = decode(row[0])
                    #print(recipe_id_list)
                    for recipe_id in recipe_id_list:
                        if recipe_id not in recipe_common_ing_count:
                            continue
                        else:
                            recipe_common_ing_count[recipe_id] -=1
                        #if int(recipe_id) == 7454:
                            #print(recipe_common_ing_count[recipe_id])
                recipe_dict = sorted(recipe_common_ing_count.items(),key=lambda k:k[1])
        json_dict = {'id':[],'length':len(recipe_dict)}
        for id in recipe_dict:
            json_dict['id'].append(id[0])
        db.close()
        print('success 1')
        return json.dumps(json_dict)
    if args['city'] == 'None':
        args = request.args
        print(args)
        recipe_ids = args['recipe_list'].strip().split(',')
        db = pymysql.connect("localhost","root","","recipes" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        json_dict = {'recipe_info':[]}
        for id in recipe_ids:
            sql = ("""SELECT image_url,description FROM recipe_info WHERE recipe_id LIKE %s""",id)
            cursor.execute(*sql)
            results = cursor.fetchall()
            for row in results:
                image_url = row[0]
                desc = row[1]
            json_dict['recipe_info'].append({'id':id,'src':image_url,'desc':desc})
        db.close()
        print('success 2')
        return json.dumps(json_dict)
@app.route("/retrieve")
def retrieve():
    args = request.args
    print(args)
    recipe_ids = args['recipe_list'].strip().split(',')
    db = pymysql.connect("localhost","root","","recipes" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    json_dict = {'recipe_info':[]}
    for id in recipe_ids:
        sql = ("""SELECT image_url,description FROM recipe_info WHERE recipe_id LIKE %s""",id)
        cursor.execute(*sql)
        results = cursor.fetchall()
        for row in results:
            image_url = row[0]
            desc = row[1]
        json_dict['recipe_info'].append({'id':id,'src':image_url,'desc':desc})
    db.close()
    print('success 2')
    return json.dumps(json_dict)
    #sq11 = ("""SELECT documents FROM ranking_pagerank WHERE word LIKE %s""", "%"+word+"%")
    """cursor.execute(*sq11)
    score = cursor.fetchone()
    v = float(v) * float(score[0])
    if k in docu_dict:
        if docu_dict[k] < v:
            docu_dict[k] = v
    else:
        docu_dict[k] = v

    total = time.time()-start
    docu_dict = sorted(docu_dict.items(),key=lambda x:x[1],reverse=True)


for k,v in docu_dict:
    print(k)
print(total)
"""
if __name__ == "__main__":
    app.run(debug=True,threaded=True)