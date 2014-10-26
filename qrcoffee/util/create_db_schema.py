#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :create_db_schema.py
#description     :This will create qr-coffee's database schema in an fresh SQLite3 database.
#                 Any exiting database will be erased, so HANDLE WITH CARE!!!
#author          :marticlaus
#date            :20141009
#version         :0.1.0
#usage           :python create_db_schema.py db_file
#notes           :
#python_version  :2.7.1
#==============================================================================

import os
import sys
from PySide import QtSql
from ..db.connection import openConnection,  closeConnection

def create_db_schema(db):
    """create_db_schema(db)
    Erases database db and creates new empty schema.
    """
    def exec_query(q_obj,  q_string):
        if not q_obj.exec_(q_string):
            print "%s:" % q_obj.lastError().driverText()
            print "Statement: %s" % q_string
            print "Database says: %s" % q_obj.lastError().databaseText()
    # delete database
    erase_db(db)
    query = QtSql.QSqlQuery()
    exec_query(query, u"CREATE TABLE person( " +
                "ID INT PRIMARY KEY NOT NULL, " +
                "name TEXT NOT NULL, " +
                "firstname TEXT NOT NULL, " +
                "tag TEXT NOT NULL);")
    exec_query(query, u"CREATE TABLE trans_type( " +
                "ID INT PRIMARY KEY NOT NULL, " + 
                "description TEXT NOT NULL);")
    exec_query(query, u"CREATE TABLE coffee_price( " +
                "ID INT PRIMARY KEY NOT NULL, " +
                "name TEXT NOT NULL DEFAULT ('coffee'), " +
                "value REAL NOT NULL, " +
                "date INTEGER(4) DEFAULT (strftime('%s','now')));")
    exec_query(query, u"CREATE TABLE product( " +
                "ID INT PRIMARY KEY NOT NULL, " +
                "description TEXT NOT NULL, " +
                "def_price REAL DEFAULT (0.));")
    exec_query(query, u"CREATE TABLE trans( " +
                "ID INT PRIMARY KEY NOT NULL, " +
                "type INT NOT NULL, " +
                "date INTEGER(4) NOT NULL DEFAULT (strftime('%s','now')), " +
                "value REAL NOT NULL, " +
                "pers_id INT, " +
                "balanced BOOLEAN NOT NULL DEFAULT (0), " +
                "FOREIGN KEY(type) REFERENCES trans_type(ID), " +
                "FOREIGN KEY(pers_id) REFERENCES person(ID));")
    exec_query(query, u"CREATE TABLE reciept_item( " +
                "ID INT PRIMARY KEY NOT NULL, " +
                "prod_id INT NOT NULL, " +
                "trans_id NOT NULL, " +
                "amount INT NOT NULL DEFAULT (1), " +
                "unit_price REAL NOT NULL, " +
                "FOREIGN KEY(prod_id) REFERENCES product(ID), " +
                "FOREIGN KEY(trans_id) REFERENCES trans(ID));")
    exec_query(query, u"CREATE VIEW coffee_list AS " +
                "SELECT p.firstname || ', ' || SUBSTR(p.name,1,1) || '.', " +
                "SUM(tt.description='coffee purchase'), " +
                "SUM(t.value) " +
                "FROM trans as t " +
                "INNER JOIN person as p ON p.ID=t.pers_id " +
                "INNER JOIN trans_type as tt ON t.type=tt.ID " +
                "WHERE t.balanced=0 " +
                "GROUP BY p.ID " +
                "ORDER BY p.firstname;")
    closeConnection(db)

def erase_db(db):
    """erase_db(db)
    Deletes database file associated with db and create a new empty file
    with the same path and a connection to it with the same connection name.
    """
    db_file = db.databaseName()
    con_name = db.connectionName()
    os.remove(db_file)
    db = openConnection(db_file,  con_name)

def main(db_file):
    db = openConnection(db_file)
    create_db_schema(db)

if __name__ == "__main__":
    main(sys.argv[1])
    
