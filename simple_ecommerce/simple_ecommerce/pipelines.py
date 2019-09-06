# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.sql import text


# e = create_engine('mysql+pymysql://root:admin@localhost/mydb')
# for row in e.execute('select * from product where id < %s', 2):
#     print(dict(row))
#
#
# # statement = text(
# #     """
# #     INSERT INTO product
# #     (id, title, price, currency)
# #     VALUES
# #     (1, 'Example', 1.99, '$')
# #     """
# # )
# #
# # conn = e.connect()
# # t = conn.begin()
# # e.execute(statement)
# # t.commit()
# # conn.close()


class MySQLPipeline(object):
    e = create_engine('mysql+pymysql://root:admin@localhost/mydb')

    temp = """
        INSERT INTO product
        (title, price, currency, image, description)
        VALUES
        ('%s', '%s', '%s', '%s', '%s')
        """

    def process_item(self, item, spider):
        statement = text(
            self.temp % (
                item['title'],
                item['price'],
                item['currency'],
                item['image'],
                item['description']
            )
        )

        conn = self.e.connect()
        t = conn.begin()
        self.e.execute(statement)
        t.commit()
        conn.close()

        return item
