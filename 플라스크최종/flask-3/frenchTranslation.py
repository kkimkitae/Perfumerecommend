import os
from perfume_dao import *
import pymysql

file_path = '/Users/nam/Desktop/pythonWorkspace/re_img'
file_names = os.listdir(file_path)
file_names

translationTable = str.maketrans("éàèùâêîôûçÊÉÀ", "eaeuaeioucEEA")

for name in file_names:
    src = os.path.join(file_path, name)
    dst = name.translate(translationTable)
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)

print(file_names[0])

# myDao = MyPerfumeDao()

# target_lst = []

# for i in range(11151, 16126):
#     target = myDao.findOne(i)
#     target = target[0]['perfume_name']
#     for name in file_names:
#         if target == name[:-4]:
#             break
        
#         if name == 'Pur Blanca Energy.jpg':
#             target_lst.append(i)

# for i in target_lst:
#     myDao.deleteOne(i)
