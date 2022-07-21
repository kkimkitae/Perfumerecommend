from glob import glob
from os import dup
import sys
import random
import math
import copy
from tkinter.tix import Tree
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text, true
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from perfume_dao import *

application = Flask(__name__)
user_taste = []
myDao = MyPerfumeDao()

idx_top = None
idx_middle = None
idx_bottom = None

@application.route("/", methods = ['GET'])
def home():
    return render_template("index.html")

@application.route("/recommend_explain", methods = ['GET'])
def get_0_page():
    return render_template("explain.html")

@application.route("/recommend_main_accord_1", methods = ['GET'])
def get_1_page():
    return render_template("recommend_main_accord_1.html")

@application.route("/recommend_main_accord_2", methods = ['POST'])
def get_2_page():
    cnt = 0
    too_many = False
    no_input = False

    if len(user_taste) >= 1:
        del(user_taste[0:])

    chosen_main_accords = request.form.getlist("scent")
    
    for i in chosen_main_accords:
        if i != '':
            main_accord_1 = i
            cnt +=1

    if cnt > 1:
        too_many = True
        return render_template("recommend_main_accord_1.html", too_many = too_many)  
    
    elif cnt == 0:
        no_input = True
        return render_template("recommend_main_accord_1.html", no_input = no_input)

    print(main_accord_1)
    user_taste.append([main_accord_1])
    print(user_taste)
    
    return render_template("recommend_main_accord_2.html")

@application.route("/recommend_main_accord_3", methods = ['POST'])
def get_3_page():
    cnt = 0
    too_many = False
    no_input = False
    duplicated = False

    if len(user_taste) >= 2:
        del(user_taste[1:])

    chosen_main_accords = request.form.getlist("scent")
    
    for i in chosen_main_accords:
        if i != '':
            main_accord_2 = i
            cnt +=1

    if cnt > 1:
        too_many = True
        return render_template("recommend_main_accord_2.html", too_many = too_many)  
    
    elif cnt == 0:
        no_input = True
        return render_template("recommend_main_accord_2.html", no_input = no_input)

    if user_taste[0][0] == main_accord_2:
        duplicated = True
        return render_template("recommend_main_accord_2.html", duplicated = duplicated)
        
    print(main_accord_2)
    user_taste.append([main_accord_2])
    print(user_taste)
    
    return render_template("recommend_main_accord_3.html")

@application.route("/recommend_brand_value", methods = ['POST'])
def get_4_page():
    cnt = 0
    too_many = False
    no_input = False

    if len(user_taste) >= 3:
        del(user_taste[2:])

    chosen_main_accords = request.form.getlist("scent")
    
    for i in chosen_main_accords:
        if i != '':
            main_accord_3 = i
            cnt +=1

    if cnt > 1:
        too_many = True
        return render_template("recommend_main_accord_3.html", too_many = too_many)  
    
    elif cnt == 0:
        no_input = True
        return render_template("recommend_main_accord_3.html", no_input = no_input)

    if user_taste[0][0] == main_accord_3 or user_taste[1][0] == main_accord_3:
        duplicated = True
        return render_template("recommend_main_accord_3.html", duplicated = duplicated)

    print(main_accord_3)
    user_taste.append([main_accord_3])
    print(user_taste)
    
    return render_template("recommend_brand_value.html")

# 브랜드일 때
@application.route("/recommend_longevity", methods = ['POST'])
def get_5_page():
    no_input = False

    if len(user_taste) >= 4:
        del(user_taste[3:])
    if(request.form.getlist('brand_value') == []):
        no_input = True
        return render_template("recommend_brand_value.html", no_input = no_input)
    user_taste.append(request.form.getlist('brand_value'))
    print(user_taste)
    return render_template("recommend_longevity.html")

# 시아쥬일 때
# @application.route("/recommend_longevity", methods = ['POST'])
# def get_5_page():
#     no_input = False

#     if len(user_taste) >= 4:
#         del(user_taste[3:])
#     if(request.form.getlist('sillage') == []):
#         no_input = True
#         return render_template("recommend_sillage.html", no_input = no_input)
#     user_taste.append(request.form.getlist('sillage'))
#     print(user_taste)
#     return render_template("recommend_longevity.html")

@application.route("/recommend_season", methods = ['POST'])
def get_6_page():
    no_input = False

    if len(user_taste) >= 5:
        del(user_taste[4:])
    if(request.form.getlist('longevity') == []):
        no_input = True
        return render_template("recommend_longevity.html", no_input = no_input)
    user_taste.append(request.form.getlist('longevity'))
    print(user_taste)
    return render_template("recommend_season.html")

@application.route("/recommended_result", methods = ['POST'])
def get_recommended_result():
    no_input = False

    if len(user_taste) >= 6:
        del(user_taste[5:])

    if(request.form.getlist('season') == []):
        no_input = True
        return render_template("recommend_season.html", no_input = no_input)

    user_taste.append(request.form.getlist('season'))
    print(user_taste)

    real_user_taste = copy.deepcopy(user_taste)

    for i in range(0,3):
        idx = real_user_taste[i][0].find('_')
        if idx == -1:
            continue
        real_user_taste[i][0] = real_user_taste[i][0][:idx]
    print(real_user_taste)

    similar_idxs = myDao.recommend(real_user_taste)

    global idx_top
    global idx_middle
    global idx_bottom

    print(len(similar_idxs))

    # 리턴 길이가 가변적이므로 맞추는 작업
    if (len(similar_idxs) % 3) == 0:
        idx_top = similar_idxs[0:len(similar_idxs)//3]
        idx_middle = similar_idxs[len(similar_idxs)//3 : 2*(len(similar_idxs)//3)]
        idx_bottom = similar_idxs[2*(len(similar_idxs)//3) : 3*(len(similar_idxs)//3)]
    elif (len(similar_idxs) % 3) == 1:
        idx_top = similar_idxs[0:math.floor(len(similar_idxs)/3) + 1]
        idx_middle = similar_idxs[math.floor(len(similar_idxs)/3) + 1 : 2*math.floor(len(similar_idxs)/3) + 1]
        idx_bottom = similar_idxs[2*math.floor(len(similar_idxs)/3) + 1 : 3*math.floor(len(similar_idxs)/3) + 1]
    else:
        idx_top = similar_idxs[0:math.floor(len(similar_idxs)/3) + 1]
        idx_middle = similar_idxs[math.floor(len(similar_idxs)/3) + 1 : 2*math.floor(len(similar_idxs)/3) + 2]
        idx_bottom = similar_idxs[2*math.floor(len(similar_idxs)/3) + 2 : 3*math.floor(len(similar_idxs)/3) + 2]

    print(len(idx_top))
    print(len(idx_middle))
    print(len(idx_bottom))

    random_top = random.choice(idx_top) + 1
    random_middle = random.choice(idx_middle) + 1
    random_bottom = random.choice(idx_bottom) + 1

    first = myDao.findOne(random_top)
    second = myDao.findOne(random_middle)
    third = myDao.findOne(random_bottom)
    
    # img1 = f'images/Chanel No 5 Eau de Parfum 100th Anniversary – Ask For The Moon Limited Edition.jpg'

    img1 = first[0]['perfume_name']
    img1 = f'images/{img1}.jpg'
    img2 = second[0]['perfume_name']
    img2 = f'images/{img2}.jpg'
    img3 = third[0]['perfume_name']
    img3 = f'images/{img3}.jpg'

    cnt = 1
    return render_template("recommended_result.html", first = first, second = second, third = third, img1 = img1, img2 = img2, img3 =img3, cnt = cnt)
    
# 동적 라우팅
@application.route("/recommended_result/re/<cnt>", methods = ['GET'])
def reget_recommended_result(cnt):
    global idx_top
    global idx_middle
    global idx_bottom

    print(len(idx_top))
    print(len(idx_middle))
    print(len(idx_bottom))

    random_top = random.choice(idx_top) + 1
    random_middle = random.choice(idx_middle) + 1
    random_bottom = random.choice(idx_bottom) + 1

    first = myDao.findOne(random_top)
    second = myDao.findOne(random_middle)
    third = myDao.findOne(random_bottom)

    img1 = first[0]['perfume_name']
    img1 = f'images/{img1}.jpg'
    img2 = second[0]['perfume_name']
    img2 = f'images/{img2}.jpg'
    img3 = third[0]['perfume_name']
    img3 = f'images/{img3}.jpg'

    cnt = int(cnt) + 1
    return render_template("recommended_result.html", first = first, second = second, third = third, img1 = img1, img2 = img2, img3 =img3, cnt = cnt)

# 향수 상세 정보 페이지로 보내주는 라우터
# 동적 라우터
@application.route("/recommended_result/<perfume_name>", methods = ['POST'])
def get_info(perfume_name):
    # print(type(request.form))
    # print(list(request.form.items())[0])

    searched_perfume_id = request.form.get("id")    
    searched_perfume = myDao.findOne(searched_perfume_id)

    img = f'images/{perfume_name}.jpg'

    return render_template("specific_info.html", searched_perfume = searched_perfume, img = img)

@application.route("/search/perfume", methods = ['GET' , 'POST'])
def search_perfume():
    no_that_perfume = False
    perfumes = myDao.findAllPerfumeName()
    if request.method == 'GET':
        return render_template("search_perfume.html", perfumes = perfumes)

    elif request.method == 'POST':
        perfume_name = request.form.get('perfume_name')
        found_perfume = myDao.findByName(perfume_name)
        if found_perfume == []:
            no_that_perfume = True
            return render_template("search_perfume.html", no_that_perfume = no_that_perfume, perfumes = perfumes)
        
        img = found_perfume[0]['perfume_name']
        img = f'images/{img}.jpg'

        return render_template("search_perfume.html", found_perfume = found_perfume, img = img, perfumes = perfumes)

@application.route("/search/perfume/<perfume_name>", methods = ['POST'])
def get_info2(perfume_name):
    searched_perfume_id = request.form.get("id")    
    searched_perfume = myDao.findOne(searched_perfume_id)

    img = f'images/{perfume_name}.jpg'

    return render_template("specific_info.html", searched_perfume = searched_perfume, img = img)

@application.route("/recommend_by_perfume", methods = ['GET', 'POST'])
def recommend_by_perfume():
    no_that_perfume = False
    perfumes = myDao.findAllPerfumeName()
    if request.method == 'GET':
        return render_template("recommend_by_perfume.html", perfumes = perfumes)

    elif request.method == 'POST':
        perfume_name = request.form.get('perfume_name')
        found_perfume = myDao.findByName(perfume_name)
        if found_perfume == []:
            no_that_perfume = True
            return render_template("recommend_by_perfume.html", no_that_perfume = no_that_perfume, perfumes = perfumes)
        
        img = found_perfume[0]['perfume_name']
        img = f'images/{img}.jpg'

        return render_template("recommend_by_perfume.html", found_perfume = found_perfume, img = img, perfumes = perfumes)

@application.route("/recommend_by_perfume/result", methods = ['POST'])
def get_recommned_by_perfume_result():
    selected_perfume_id = request.form.get('id')
    selected_perfume = myDao.findOneFromPP(selected_perfume_id)
    selected_perfume_features = [[selected_perfume[0]['main_accord1']], [selected_perfume[0]['main_accord2']], [selected_perfume[0]['main_accord3']], [selected_perfume[0]['brand_value']], [selected_perfume[0]['longevity']], [selected_perfume[0]['season']]]

    similar_idxs = myDao.recommend(selected_perfume_features)

    global idx_top
    global idx_middle
    global idx_bottom

    print(len(similar_idxs))

    # 리턴 길이가 가변적이므로 맞추는 작업
    if (len(similar_idxs) % 3) == 0:
        idx_top = similar_idxs[0:len(similar_idxs)//3]
        idx_middle = similar_idxs[len(similar_idxs)//3 : 2*(len(similar_idxs)//3)]
        idx_bottom = similar_idxs[2*(len(similar_idxs)//3) : 3*(len(similar_idxs)//3)]
    elif (len(similar_idxs) % 3) == 1:
        idx_top = similar_idxs[0:math.floor(len(similar_idxs)/3) + 1]
        idx_middle = similar_idxs[math.floor(len(similar_idxs)/3) + 1 : 2*math.floor(len(similar_idxs)/3) + 1]
        idx_bottom = similar_idxs[2*math.floor(len(similar_idxs)/3) + 1 : 3*math.floor(len(similar_idxs)/3) + 1]
    else:
        idx_top = similar_idxs[0:math.floor(len(similar_idxs)/3) + 1]
        idx_middle = similar_idxs[math.floor(len(similar_idxs)/3) + 1 : 2*math.floor(len(similar_idxs)/3) + 2]
        idx_bottom = similar_idxs[2*math.floor(len(similar_idxs)/3) + 2 : 3*math.floor(len(similar_idxs)/3) + 2]

    print(len(idx_top))
    print(len(idx_middle))
    print(len(idx_bottom))

    random_top = random.choice(idx_top) + 1
    random_middle = random.choice(idx_middle) + 1
    random_bottom = random.choice(idx_bottom) + 1

    first = myDao.findOne(random_top)
    second = myDao.findOne(random_middle)
    third = myDao.findOne(random_bottom)
    
    img1 = first[0]['perfume_name']
    img1 = f'images/{img1}.jpg'
    img2 = second[0]['perfume_name']
    img2 = f'images/{img2}.jpg'
    img3 = third[0]['perfume_name']
    img3 = f'images/{img3}.jpg'

    cnt = 1
    return render_template("recommended_result.html", first = first, second = second, third = third, img1 = img1, img2 = img2, img3 =img3, cnt = cnt)

# 동적 라우팅
@application.route("/recommend_by_perfume/result/re/<cnt>", methods = ['GET'])
def reget_recommned_by_perfume_result(cnt):
    global idx_top
    global idx_middle
    global idx_bottom

    print(len(idx_top))
    print(len(idx_middle))
    print(len(idx_bottom))

    random_top = random.choice(idx_top) + 1
    random_middle = random.choice(idx_middle) + 1
    random_bottom = random.choice(idx_bottom) + 1

    first = myDao.findOne(random_top)
    second = myDao.findOne(random_middle)
    third = myDao.findOne(random_bottom)

    img1 = first[0]['perfume_name']
    img1 = f'images/{img1}.jpg'
    img2 = second[0]['perfume_name']
    img2 = f'images/{img2}.jpg'
    img3 = third[0]['perfume_name']
    img3 = f'images/{img3}.jpg'

    cnt = int(cnt) + 1
    return render_template("recommended_result.html", first = first, second = second, third = third, img1 = img1, img2 = img2, img3 =img3, cnt = cnt)

# 향수 상세 정보 페이지로 보내주는 라우터
# 동적 라우터
@application.route("/recommend_by_perfume/result/<perfume_name>", methods = ['POST'])
def get_info3(perfume_name):
    searched_perfume_id = request.form.get("id")    
    searched_perfume = myDao.findOne(searched_perfume_id)

    img = f'images/{perfume_name}.jpg'

    return render_template("specific_info.html", searched_perfume = searched_perfume, img = img)

@application.route("/to_home", methods = ['GET'])
def to_home():
    return redirect(url_for('home'))

@application.route("/perfume_dict")
def perfume_dict():
    return render_template("perfume_dict.html")

@application.route("/perfumes")
def perfumes():
    return render_template("perfumes.html")    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port = 8000)