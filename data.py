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

questions = []
for line in data_questions:
    ans = line.split("\n")

    q, a1, a2, a3, a4 = ans[0], ans[1], ans[2], ans[3], ans[4]
    questions.append([q, [a1, a2, a3, a4]])
print(questions)
