data_questions = [
    """"What is the capital of Italy:
Rome
Paris
Tokyio
Madrid""",

    """What is the capital of France:
Paris
Rome
Tokyio
Madrid""",

    """What is the capital of England:
London
Paris
Tokyio
Madrid""",
]
import pandas as pd
import csv
with open('questions.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
df = pd.read_csv("questions.csv", encoding='utf-8')
questions = []
# for line in data_questions:
#     ans = line.split("\n")

#     q, a1, a2, a3, a4 = ans[0], ans[1], ans[2], ans[3], ans[4]
#     questions.append([q, [a1, a2, a3, a4]])
# print(questions)
print(df)
for i in range(len(df)) :
    q = df['aws'][i]
    a1,a2,a3,a4 = df['A'][i], df['B'][i], df['C'][i], df['D'][i]
    questions.append([q, [a1, a2, a3, a4]])
print(questions)
