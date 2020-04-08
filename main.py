import pandas as pd
import os
import zipfile
import mysql.connector
from flask import Flask, render_template

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
file = os.listdir(r"D:\Users\USER\IdeaProjects\FindText\file")[0]
filename, file_extension = os.path.splitext(file)

# looping to add new row by file name
# for n in range(5):
#     count_round = 0
#     if count_round <= 100:
#         df_two = pd.DataFrame({'word': n[filename]})
#     count_round += 1
#
# print(len(df_two.axes[0]))
# print(df_two)

# create new column for word of length
df['length'] = df['word'].str.len()

# convert to lower case
df = df.apply(lambda x: x.astype(str).str.lower())

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
for letter, group in df.groupby(firstletter):
    group.to_csv("folder/dictionary_{}.txt".format(letter))
    zipfile.ZipFile("zip/dictionary_{}.zip".format(letter), 'w').write("folder/dictionary_{}.txt".format(letter))

# check size of file in folder
sizes = os.path.getsize("folder/dictionary_A.txt")
# print(sizes)

# connect mysql database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234"
)
# check database connection
# print(mydb.is_connected())


app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")
#
#
# @app.route("/salvador")
# def salvador():
#     return "Hello, Salvador"
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
