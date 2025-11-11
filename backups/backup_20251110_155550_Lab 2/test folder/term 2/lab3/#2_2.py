import math
def to_bytes(size, unit):
    if unit == "B":
        return size
    elif unit == "KB":
        return size * 1024
    elif unit == "MB":
        return size * 1024 * 1024
    elif unit == "GB":
        return size * 1024 * 1024 * 1024
    else:
        return 0
def to_largest_unit(size_in_bytes):
    if size_in_bytes >= 1024 * 1024 * 1024:
        return f"{round(size_in_bytes / (1024 * 1024 * 1024))} GB"
    elif size_in_bytes >= 1024 * 1024:
        return f"{round(size_in_bytes / (1024 * 1024))} MB"
    elif size_in_bytes >= 1024:
        return f"{round(size_in_bytes / 1024)} KB"
    else:
        return f"{size_in_bytes} B"
with open('/home/danina/Repositories/Study/term 2/lab3/input.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
files_by_extension = {}
for line in lines:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    filename = parts[0]
    size = int(parts[1])
    unit = parts[2]
    size_in_bytes = to_bytes(size, unit)

    extension = filename.split('.')[-1]

    if extension not in files_by_extension:
        files_by_extension[extension] = {"files": [], "total_size": 0}
    files_by_extension[extension]["files"].append(filename)
    files_by_extension[extension]["total_size"] += size_in_bytes

sorted_extensions = sorted(files_by_extension.keys())

with open('/home/danina/Repositories/Study/term 2/lab3/output.txt', 'w', encoding='utf-8') as output_file:
    for extension in sorted_extensions:
        files_by_extension[extension]["files"].sort()

        for filename in files_by_extension[extension]["files"]:
            output_file.write(f"{filename}\n")

        total_size = files_by_extension[extension]["total_size"]
        summary = to_largest_unit(total_size)

        output_file.write("----------\n")
        output_file.write(f"Summary: {summary}\n")