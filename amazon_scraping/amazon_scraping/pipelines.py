# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonScrapingPipeline:
    def process_item(self,item,spider):
        adapter = ItemAdapter(item)

        # clean prices make it an integer 
        price = adapter.get('price')
        adapter['price'] = float(price)

        # clean stars 
        stars = adapter.get('stars')
        stars_string = stars.split(' ')
        stars = stars_string[0]
        adapter['stars'] = float(stars)

        # # rating count
        rating_count = adapter.get('rating_count')
        rating_count_string = rating_count.split(' ')
        rating_count = rating_count_string[0]
        if "," in rating_count:
            rating_count = rating_count.replace(',','')
        adapter['rating_count'] = float(rating_count)




        return item
    


# import mysql.connector

# class SaveToMySQLPipeline:

#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='mysqlmysql29',
#             database='amazon'
#         )

#         ## Create cursor, used to execute commands
#         self.cur = self.conn.cursor()
        
#          ## Create product table if none exists
#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS product(
#             id int NOT NULL auto_increment, 
#             name VARCHAR(255),
#             relative_url VARCHAR(255),
#             price DECIMAL,
#             stars DECIMAL,
#             rating_count DECIMAL,
#             feature_bullets text,
#             PRIMARY KEY (id)
#         )
#         """)

#     def process_item(self, item, spider):

#         ## Define insert statement
#         self.cur.execute(""" insert into product (
#             name, 
#             relative_url, 
#             price, 
#             stars, 
#             rating_count,
#             feature_bullets
#             ) values (
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s
#                 )""", (
#             item["name"],
#             item["relative_url"],
#             item["price"],
#             item["stars"],
#             item["rating_count"],
#             item["feature_bullets"]
#         ))

#         ## Execute insert of data into database
#         self.conn.commit()
#         return item

    
#     def close_spider(self, spider):

#         ## Close cursor & connection to database 
#         self.cur.close()
#         self.conn.close()
