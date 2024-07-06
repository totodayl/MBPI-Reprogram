from datetime import datetime

# Assuming time_start and time_end are lists containing datetime strings
time_start = ["2024-06-01 10:00:00"]
time_end = ["2024-06-03 08:00:00"]

# Convert strings to datetime objects
start = datetime.strptime(time_start[0], "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(time_end[0], "%Y-%m-%d %H:%M:%S")

# Calculate time difference
time_difference = start - end

# Get total time without days
total_seconds = time_difference.total_seconds()
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

print("Total time without days:", int(hours), "hours", int(minutes), "minutes", int(seconds), "seconds")
