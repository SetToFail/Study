# Чтение данных из файла pipes.txt
with open('pipes.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
pipes_data = []
used_pipes = []
is_pipes_list = False
for line in lines:
    line = line.strip()
    if not line:
        is_pipes_list = True
        continue
    if is_pipes_list:
        used_pipes = list(map(int, line.split()))
    else:
        pipes_data.append(float(line))
total_speed = 0
for pipe in used_pipes:
    # Номер трубы соответствует индексу + 1
    pipe_index = pipe - 1
    if 0 <= pipe_index < len(pipes_data):
        total_speed += 1 / pipes_data[pipe_index]
if total_speed > 0:
    total_time_hours = 1 / total_speed
else:
    total_time_hours = 0
total_time_minutes = total_time_hours * 60
with open('time.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(f"{total_time_minutes}")