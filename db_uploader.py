import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Section,Category,Type,Fit,Description,Product,ProductColor,ProductSize,Color,Size,Image

CSV_PATH_PRODUCTS = './lafesta.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file) #데이터에서 한줄씩 
    next(data_reader,None) #첫번째 head부분 row값 뺌 
    
    for row in data_reader:
        #row csv파일 한줄씩 출력 
        if row[0]: #section,women,men이 나타남 
            firstrow = row[0]
            Fit.objects.create(name = firstrow)
            # firstrow = row[0] #csv 첫번째 줄 
            # secondrow = row[1] # csv 두번째 줄
            # third_row = row[2]
            # fourth_row = row[3]
            # fifth_row = row[4]
            # Product.objects.create(name = firstrow, price=secondrow, type_id=third_row,fit_id= fourth_row,description_id=fifth_row)
        
        # category_name= row[1]
        # section_id = Section.objects.get(name= section_name).id
        
        # Category.objects.create(name= category_name, section_id = section_id)

        # type_name=row[2]
        # category_id = Category.objects.get(name=type_name).id

        # Type.objects.create(name=type_name, category_id= category_id)
        
        # if row[2]:
        #     type_name = row[2]
        #     Type.objects.create(name = type_name)
        # if row[3]:
        #     fit_name = row[3]
        #     Fit.objects.create(name = fit_name)
