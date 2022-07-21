from re import A
import pymysql
import numpy as np
import pandas as pd
import random
import math
import copy 
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from perfume_dao import MyPerfumeDao

# a =[[1],[2],[3]]
# b = copy.deepcopy(a)

# b[0][0] = 10
# print(a)
# print(b)

myDao = MyPerfumeDao()
print(myDao.findByName("이건 없잖아"))
# print(myDao.findOne(1))
