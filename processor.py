def process(file, date):
    counts = parse_input_file(file, date)
    most_active_cookies = find_most_active_cookies(counts)

    for cookie in most_active_cookies:
        print(cookie)
def parse_input_file(file_path, target_date):
    counts = {}

    with open(file_path, "r") as file:
        next(file)

        for line in file:
            cookie, timestamp = line.split(",")
            date = timestamp.split("T")[0]

            if date == target_date:
                counts[cookie] = counts.get(cookie, 0) + 1

            elif date < target_date:
                break # break early

    return counts

def find_most_active_cookies(counts):
    if not counts:
        raise ValueError("No cookies found")

    most_active_count = max(counts.values())
    return [cookie for cookie, count in counts.items() if count == most_active_count]