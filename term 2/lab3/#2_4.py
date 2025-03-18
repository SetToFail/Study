import csv
n, m = map(int, input().split())
eligible_students = []
while True:
    try:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        surname, name, *scores = parts
        scores = list(map(int, scores))
        total = sum(scores)
        if total >= n and all(score >= m for score in scores):
            eligible_students.append([surname, name] + scores + [total])
    except EOFError:
        break
with open('/home/danina/Загрузки/Telegram Desktop/lab3/exam.csv', 'w', encoding='cp1251', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Фамилия", "имя", "результат 1", "результат 2", "результат 3", "сумма"])
    writer.writerows(eligible_students)