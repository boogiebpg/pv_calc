import csv
import sys
from datetime import datetime, date

def calculate_pv_generation(file_handler):
    with file_handler as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        pv_data = []
        for row in reader:
            if len(row) < 2:  # Skip empty or invalid rows
                continue
            time_str, power_str = row

            # Check if power_str is not empty before converting to float
            if power_str.strip() == '':
                continue

            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            try:
                power = float(power_str)
            except ValueError:
                continue  # Skip invalid float conversion

            pv_data.append((time, power))

    # Detect the time interval (in hours) between measurements
    if len(pv_data) > 1:
        time_diff = (pv_data[1][0] - pv_data[0][0]).total_seconds() / 3600
    else:
        time_diff = 1  # Default to 1 hour if there's only one entry

    print(f"Time interval: {round(time_diff*60)} minutes")

    # Calculate daily generation and keep only full days
    daily_data = {}
    for time, power in pv_data:
        day = time.date()
        if day not in daily_data:
            daily_data[day] = []
        daily_data[day].append(power * time_diff)

    # Determine expected number of entries per day
    expected_entries_per_day = int(24 / time_diff)

    # Write the results to result.txt (only for full days)
    with open('result.txt', 'w') as result_file:
        for day, power_values in daily_data.items():
            print(f"{day}, intervals count: {len(power_values)},", end=" ")
            if len(power_values) >= expected_entries_per_day or day == date.today():  # Only include full days and today, also take into account possible time shift 2 times per year
                total_power = sum(power_values)
                kwh = round(total_power / 1000, 2)  # Convert to kWh and round to 2 digits
                result_file.write(f"{day} {kwh}\n")
                print(f"included: yes, kwh: {kwh}")
            else:
                print("included: NO")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: pv_calc.py <csv_file>")
        sys.exit(1)

    try:
        csv_file = sys.argv[1]
        file_handler = open(csv_file, 'r')
    except FileNotFoundError:
        print("File Not Found.")
        sys.exit(1)

    calculate_pv_generation(file_handler)

