import pandas as pd
import os
import zipfile
import mysql.connector
from flask import Flask, redirect, url_for, request, render_template
import time

# import file dictionary
# f = open(r"file/word.txt", encoding="utf8").readlines()
# remove \n in data
# f = [x.strip() for x in f]
# print(f)

# import file dictionary
df = pd.read_csv("file/word.txt", sep="\n", header=None)
# df = pd.DataFrame(f)
df.columns = ["word"]

# get file name to filename
file = os.listdir(r"D:\Users\USER\IdeaProjects\dictionary\file")[0]
filename, file_extension = os.path.splitext(file)

# looping to add new row by file name
# for n in range(5):
#     count_round = 0
#     if count_round <= 100:
#         df_two = pd.DataFrame({'word': n[filename]})
#     count_round += 1
# print(len(df_two.axes[0]))
# print(df_two)

# create new column for word of length
df['length'] = df['word'].str.len()

# convert to lower case
df = df.apply(lambda x: x.astype(str).str.lower())

# for root, dirs, files in os.listdir(r"folder/dictionary_A.txt"):
#     for file in files:
#         if file.endswith(".txt"):
#             print(os.path.join("file", file))

df['length'] = pd.to_numeric(df['length'])
# check length of word > 5
print('check length of word > 5 is ' + str(len(df[df.length > 5])))

# compare first between last word
df['first_word'] = df['word'].astype(str).str[0]
df['last_word'] = df['word'].astype(str).str[-1]
print("compare first between last word is " + str(len(df[df.first_word == df['last_word']])))

# convert to first character to upper case
df['word'] = df.word.str.title()

# get character to create folder
df_first = df[df['word'].str.len() == 1].word
df_first.reset_index(drop=True, inplace=True)
df_first.columns = ["alphabet"]

df = df.drop(columns=["length", "first_word", "last_word"], axis=1)


# get first word from df
def firstletter(index):
    # df.reset_index(drop=True)
    firstentry = df.iloc[index, 0]
    return firstentry[0]


# create file and zip file by first character
# check size of file in folder
for letter, group in df.groupby(firstletter):
    group.to_csv("folder/dictionary_{}.txt".format(letter), index=False)
    zipfile.ZipFile("zip/dictionary_{}.zip".format(letter), 'w').write("folder/dictionary_{}.txt".format(letter))
    filesizes = os.stat("folder/dictionary_{}.txt".format(letter)).st_size
    zipsizes = os.stat("zip/dictionary_{}.zip".format(letter)).st_size
    print("size of file dictionary_{}.txt is ".format(letter) + str(filesizes))
    print("size of zip file dictionary_{}.zip is ".format(letter) + str(zipsizes))
    diffsize = ((zipsizes - filesizes) / filesizes) * 100
    diffsize = float("{:.2f}".format(diffsize))
    print("percent different is " + str(diffsize) + " %")

# connect mysql database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234"
)
# check database connection
# print(db.is_connected())

# insert file to table
cursor = db.cursor()
# cursor.execute("TRUNCATE TABLE table")

folder = open(r'folder/dictionary_A.txt')
file_content = folder.read().strip()

# print(file_content)
# values = pd.DataFrame(eval(file_content))
folder.close()
# print(values)

query = "INSERT INTO table VALUES (%s)"

# cursor.execute(query, values)
# cursor.execute(query, (file_content,))

db.commit()
db.close()

# test Flask
app = Flask(__name__)  # create an app instance


@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


if __name__ == "__main__":  # on running python app.py
    app.run()  # run the flask app


start_time = time.time()
# main()
print("--- runtime is %s seconds ---" % (time.time() - start_time))
