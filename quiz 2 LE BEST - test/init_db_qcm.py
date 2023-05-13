# -*- coding: utf-8 -*-
"""
Created on Mon May  8 22:43:32 2023

@author: jugur
"""

import sqlite3

connection = sqlite3.connect('database_qcm.db')


with open('schema_qcm.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO questions (id, qcm, question, answer) VALUES (?, ?, ?, ?)",
            (1, 1, "bah ducon frere?", "Hyper Text Markup Language")
            )

options = [
    (1, "Hyper Text Preprocessor"),
    (1, "Hyper Text Markup Language"),
    (1, "Hyper Text Multiple Language"),
    (1, "Hyper Tool Multi Language")
]

cur.executemany("INSERT INTO options (question_id, option) VALUES (?, ?)", options)


connection.commit()
connection.close()
