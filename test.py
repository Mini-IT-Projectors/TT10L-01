import csv
username = 'Suhaini Binti Nordin'
with open('lecturer.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['username'] == username:
            subject = row['subject']  # Access the subject column
            print(f"The subject for Suhaini Binti Nordin is: {subject}")
            break