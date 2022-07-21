from email.errors import MissingHeaderBodySeparatorDefect
import pymysql
import numpy as np
import pandas as pd
import random
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

class MyPerfumeDao:
    def __init__(self):
        pass

    def deleteOne(self, target_id):
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        sql = "delete from perfume where id = {};".format(target_id)
        curs.execute(sql)
        
        db.commit()
        db.close()

    def findOne(self, target_id):
        ret = []
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        sql = "select * from perfume where id = {};".format(target_id)
        curs.execute(sql)
        
        rows = curs.fetchall()
        for p in rows:
            temp = {'id':p[0],'perfume_name':p[1],'brand':p[2], 'brand_value' : p[3], 'gender':p[4], 'launch_year':p[5], 'main_accord1':p[6], 'main_accord2':p[7], 'main_accord3':p[8], 'top_note':p[9],
            'middle_note':p[10], 'base_note':p[11], 'season':p[12], 'day_or_night':p[13], 'longevity':p[14], 'sillage':p[15], 
            'rating':p[16], 'voters_num':p[17], 'main_accord1_ratio':p[18], 'main_accord2_ratio':p[19], 'main_accord3_ratio':p[20]}
            ret.append(temp)
        
        db.commit()
        db.close()
        return ret

    def findOneFromPP(self, target_id):
        ret = []
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        sql = "select * from preprocessed_perfume where id = {};".format(target_id)
        curs.execute(sql)
        
        rows = curs.fetchall()
        for p in rows:
            temp = {'id':p[0],'perfume_name':p[1], 'brand_value' : p[2], 'main_accord1':p[3], 'main_accord2':p[4], 'main_accord3':p[5], 'season':p[6], 
            'longevity':p[7], 'rating':p[8], 'voters_num':p[9], 
            'main_accord1_ratio':p[10], 'main_accord2_ratio':p[11], 'main_accord3_ratio':p[12]}
            ret.append(temp)
        
        db.commit()
        db.close()
        return ret

    def findAll(self):
        ret = []
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        sql = "select * from perfume;"
        curs.execute(sql)
        
        rows = curs.fetchall()
        for p in rows:
            temp = {'id':p[0],'perfume_name':p[1],'brand':p[2], 'brand_value' : p[3], 'gender':p[4], 'launch_year':p[5], 'main_accord1':p[6], 'main_accord2':p[7], 'main_accord3':p[8], 'top_note':p[9],
            'middle_note':p[10], 'base_note':p[11], 'season':p[12], 'day_or_night':p[13], 'longevity':p[14], 'sillage':p[15], 
            'rating':p[16], 'voters_num':p[17], 'main_accord1_ratio':p[18], 'main_accord2_ratio':p[19], 'main_accord3_ratio':p[20]}
            ret.append(temp)

        db.commit()
        db.close()
        return ret

    def findAllPerfumeName(self):
        ret = []
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        sql = "select perfume_name from perfume;"
        curs.execute(sql)
        rows = curs.fetchall()
        for p in rows:
            ret.append(p[0])

        db.commit()
        db.close()
        return ret

    def findByName(self, perfume_name):
        ret = []
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306)
        curs = db.cursor()
        
        if perfume_name.find("\'"):
            perfume_name = perfume_name.replace('\'', '\\\'')            

        perfume_name = "\'" + perfume_name + "\'"
        sql = "select * from perfume where perfume_name = {};".format(perfume_name)
        curs.execute(sql)
        
        rows = curs.fetchall()
        for p in rows:
            temp = {'id':p[0],'perfume_name':p[1],'brand':p[2], 'brand_value' : p[3], 'gender':p[4], 'launch_year':p[5], 'main_accord1':p[6], 'main_accord2':p[7], 'main_accord3':p[8], 'top_note':p[9],
            'middle_note':p[10], 'base_note':p[11], 'season':p[12], 'day_or_night':p[13], 'longevity':p[14], 'sillage':p[15], 
            'rating':p[16], 'voters_num':p[17], 'main_accord1_ratio':p[18], 'main_accord2_ratio':p[19], 'main_accord3_ratio':p[20]}
            ret.append(temp)
        
        db.commit()
        db.close()
        return ret

    def getInputVector(self, main_accord1, main_accord2, main_accord3, brand_value, longevity, season):
        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306, cursorclass=pymysql.cursors.DictCursor)
        curs = db.cursor()
        sql = "select perfume_name, brand_value, main_accord1, main_accord2, main_accord3, season, longevity, rating, voters_num, main_accord1_ratio, main_accord2_ratio, main_accord3_ratio from preprocessed_perfume;"
        curs.execute(sql)
        perfume = pd.DataFrame(curs.fetchall())

        input = f"{main_accord1} {main_accord2} {main_accord3} {brand_value} {longevity} {season}"
        voca = "brand_value longevity normal popular luxury season spices whiteflowers sweetsandgourmandsmells spring moderate muskamberanimalicsmells citrussmells winter long_lasting weak woodsandmosses summer greensherbsandfougeres fruitsvegetablesandnuts very_weak fall flowers naturalandsyntheticpopularandweird eternal resinsandbalsams beverages"
        all = [input, voca]

        input_list = input.split(" ")

        count_vector = CountVectorizer(min_df=1, ngram_range=(1,1))
        simple_vector = count_vector.fit_transform(all)
        simple_vector = simple_vector[0].toarray().astype(np.float64)
        simple_vector = simple_vector[0]

        reverse_vocabulary = dict(map(reversed, count_vector.vocabulary_.items()))

        for i in range(0, simple_vector.size):
            if (simple_vector[i] == 1):
                if i == 0: #beverage
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                
                elif i == 2: #citrus smells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 3: #eternal
                    simple_vector[i] = 0
                    simple_vector[9] = 2.5 #9 = longevity
                    continue
                    
                elif i == 4: #fall
                    simple_vector[i] = 0
                    if season == 'fall':
                        # simple_vector[17] = 0.05 # 17 = season
                        simple_vector[17] = 0.46 # 17 = season
                    continue
                    
                elif i == 5: #flowers
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue

                elif i == 6: #fruitsvegetablesandnuts
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue

                elif i == 7: #greensherbsandfougeres
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 8: #long_lasting
                    simple_vector[i] = 0
                    simple_vector[9] = 2 #9 = longevity
                    continue
                    
                elif i == 10: #luxury
                    simple_vector[i] = 0
                    simple_vector[1] = 1.59
                    continue
                        
                elif i == 11: #moderate
                    simple_vector[i] = 0
                    simple_vector[9] = 1.5 #9 = longevity
                    continue
                    
                elif i == 12: #muskamberanimalicsmells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 13: #naturalandsyntheticpopularandweird
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 14: #normal
                    simple_vector[i] = 0
                    simple_vector[1] = 0.53
                    continue

                elif i == 15: #popular
                    simple_vector[i] = 0
                    simple_vector[1] = 1.06
                    continue

                elif i == 16: #resinsandbalsams
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 18: #spices
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 19: #spring
                    simple_vector[i] = 0
                    if season == 'spring':
                        # simple_vector[17] = 0.05 # 17 = season
                        simple_vector[17] = 0.46 # 17 = season
                    continue
                    
                elif i == 20: #summer
                    simple_vector[i] = 0
                    if season == 'summer':
                        # simple_vector[17] = 0.05 # 17 = season
                        simple_vector[17] = 0.46 # 17 = season
                    continue
                
                elif i == 21: #sweetsandgourmandsmells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                    
                elif i == 22: #very_weak
                    simple_vector[i] = 0
                    simple_vector[9] = 0.5 #10 = longevity
                    continue
                    
                elif i == 23: #weak
                    simple_vector[i] = 0
                    simple_vector[9] = 1 #10 = longevity
                    continue
                    
                elif i == 24: #whiteflowers
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                        
                elif i == 25: #winter
                    simple_vector[i] = 0
                    if season == 'winter':
                        # simple_vector[17] = 0.05 # 17 = season
                        simple_vector[17] = 0.46 # 17 = season
                    continue
                    
                elif i == 26: #woodsandmosses
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.39
                    elif input_list[1].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.33
                    elif input_list[2].lower() == reverse_vocabulary[i]:
                        simple_vector[i] = 0.28
                    continue
                  
            elif simple_vector[i] == 2: # 메인 어코드가 2개 겹칠 경우
                if i == 0: #beverage
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                        
                elif i == 2: #citrus smells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                        
                elif i == 5: #flowers
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                        
                elif i == 6: #fruitsvegetablesandnuts
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue

                elif i == 7: #greensherbsandfougeres
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                        
                elif i == 12: #muskamberanimalicsmells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                    
                elif i == 13: #naturalandsyntheticpopularandweird
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                    
                elif i == 16: #resinsandbalsams
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                    
                elif i == 18: #spices
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
                    
                elif i == 21: #sweetsandgourmandsmells
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue

                elif i == 24: #whiteflowers
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue

                elif i == 26: #woodsandmosses
                    if input_list[0].lower() == reverse_vocabulary[i]:
                        temp = 0.39
                        if input_list[1].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.33 + temp
                        elif input_list[2].lower() == reverse_vocabulary[i]:
                            simple_vector[i] = 0.28 + temp
                    else:
                        simple_vector[i] = 0.61
                    continue
 
            elif simple_vector[i] == 3: #메인 어코드 카테고리가 3개 다 같을 경우
                if i == 0: #beverage
                    simple_vector[i] = 1.00
                    continue
                    
                elif i == 2: #citrus smells
                    simple_vector[i] = 1.00
                    continue
 
                elif i == 5: #flowers
                    simple_vector[i] = 1.00
                    continue  

                elif i == 6: #fruitsvegetablesandnuts
                    simple_vector[i] = 1.00
                    continue
                    
                elif i == 7: #greensherbsandfougeres
                    simple_vector[i] = 1.00
                    continue
                    
                elif i == 12: #muskamberanimalicsmells
                    simple_vector[i] = 1.00
                    continue

                elif i == 13: #naturalandsyntheticpopularandweird
                    simple_vector[i] = 1.00
                    continue
                    
                elif i == 16: #resinsandbalsams
                    simple_vector[i] = 1.00
                    continue
                
                elif i == 18: #spices
                    simple_vector[i] = 1.00
                    continue

                elif i == 21: #sweetsandgourmandsmells
                    simple_vector[i] = 1.00
                    continue
   
                elif i == 24: #whiteflowers
                    simple_vector[i] = 1.00
                    continue

                elif i == 26: #woodsandmosses
                    simple_vector[i] = 1.00
                    continue        
        db.commit()
        db.close()
        processed_input_vector = simple_vector
        return processed_input_vector

    def find_sim_perfume(self, df, sorted_idx, target_perfume, perfume_sim):
            threshold = None

            target = df[df['perfume_name'] == target_perfume]
            target_idx = target.index.values

            # 여기서 추천 샘플
            # similar_idxs = sorted_idx[sorted_idx != target_idx]
            # similar_idxs = similar_idxs[0:101]
            # df.iloc[similar_idxs].to_csv("2-1.csv")

            similar_idxs = sorted_idx[sorted_idx != target_idx]
       
            for i in range(0, similar_idxs.size):
                if perfume_sim[-1][similar_idxs[i]] < 0.93:
                    print(perfume_sim[-1][similar_idxs[i]])
                    threshold = i
                    break

            # 필터링 하기 전 전체 
            # print(type(similar_idxs))
            # print(similar_idxs)
            # print(similar_idxs.size)
            
            similar_idxs = similar_idxs[0:threshold]

            # 유사도 기준으로 필터링한 후의 남은 개수
            # print(type(similar_idxs))
            # print(similar_idxs)
            # print(threshold, "++쓰레쉬홀드++")
            # print(similar_idxs.size)
            
            df = df.iloc[similar_idxs].sort_values("weighted_rating", ascending = False)
            similar_idxs = df.index.tolist()

            return similar_idxs

    def recommend(self, user_taste):
        start = time.time()

        myDao = MyPerfumeDao()

        data_to_insert = {'perfume_name' : "user_input", 'main_accord1': user_taste[0][0], 'main_accord2' : user_taste[1][0], 'main_accord3' : user_taste[2][0], "season" : user_taste[5][0],
        "longevity" : user_taste[4][0], "brand_value" : user_taste[3][0], "rating" : None, "voters_num" : None, "main_accord1_ratio" : 0.39, "main_accord2_ratio" : 0.33, "main_accord3_ratio" : 0.28}

        db = pymysql.connect(host='localhost', user='root', db='perfume', password='epqpvmqlqjs', charset='utf8', port=3306, cursorclass=pymysql.cursors.DictCursor)
        curs = db.cursor()
        sql = "select * from perfume_mat_{};".format(data_to_insert['season'])
        curs.execute(sql)
        perfume_mat = pd.DataFrame(curs.fetchall())
        del perfume_mat['id']
        perfume_mat = perfume_mat.to_numpy()

        sql = "select perfume_name, brand_value, main_accord1, main_accord2, main_accord3, season, longevity, rating, voters_num, main_accord1_ratio, main_accord2_ratio, main_accord3_ratio from preprocessed_perfume;"
        curs.execute(sql)
        perfume = pd.DataFrame(curs.fetchall())
        print("여기6? :", time.time() - start) 
     
        processed_input_vector = myDao.getInputVector(data_to_insert['main_accord1'], data_to_insert['main_accord2'], data_to_insert['main_accord3'], data_to_insert['brand_value'], data_to_insert['longevity'], data_to_insert['season'])
        processed_input_vector = processed_input_vector.reshape(1,27)
        perfume_mat = np.concatenate((perfume_mat, processed_input_vector), axis = 0)
        print("여기5? :", time.time() - start) 
    
        perfume_sim = cosine_similarity(perfume_mat, perfume_mat)
        print("여기4? :", time.time() - start) 

        target_perfume_sim = perfume_sim[-1].reshape(-1)

        perfume_sim_sorted_idx = target_perfume_sim.argsort()[::-1]
        print("여기3? :", time.time() - start) 

        # 가중 평점(Weighted Rating) = (v/(v+m)) * R + (m/(v+m)) * C
        C = perfume['rating'].mean()
        m = perfume['voters_num'].quantile(0.6)
        print(round(C, 3), round(m, 3))

        def set_weighted_rating(row):
            v = row['voters_num']
            R = row['rating']

            return ((v/(v+m)) * R + (m/(v+m)) * C)

        perfume['weighted_rating'] = perfume.apply(set_weighted_rating, axis=1)
        print("여기2? :", time.time() - start) 
        perfume = perfume.append(data_to_insert, ignore_index=True) # input data를 perfumes에 다시 넣기

        db.commit()
        db.close()

        print("걸린 시간 :", time.time() - start) 
        return myDao.find_sim_perfume(perfume, perfume_sim_sorted_idx, 'user_input', perfume_sim)