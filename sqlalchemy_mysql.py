#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pymysql
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, String, Integer




if __name__ == "__main__":
    connection = pymysql.connect(host='127.0.0.1',
                             user='account',
                             password='password',
                             db='cindy',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
        
    """
    engine=create_engine("mysql+pymysql://account:password@127.0.0.1:80/cindy",echo=True)

    metadata = MetaData(engine)
    table_name = Table(
        'table_name',metadata,
        Column('id', Integer, primary_key=True),
        Column('age', Integer),
        Column('memo', String(20), nullable=True),
      )
    metadata.create_all()

    """
