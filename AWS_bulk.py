import csv
import requests


USER=input("Enter your Red Hat console Username")
PASSWORD=input("Enter your Red Hat console Password")



# Perform authentication check against console.redhat.com
response = requests.get('https://console.redhat.com/api/sources/v3.1/', auth=(USER, PASSWORD))
if response.status_code != 200:
    print("Authentication failed - check your USER/PASSWORD variables.")
    exit(1)

# Set INPUT to read from a different CSV file (default: "accounts.csv")
INPUT = "accounts.csv"

try:
    # Open the input CSV file
    with open(INPUT, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            name, aws_access_key_id, aws_secret_access_key = row

            # Create AWS source in RHEL Management Application
            source_data = {
                "source": {
                    "name": name,
                    "access_key_id": aws_access_key_id,
                    "secret_access_key": aws_secret_access_key,
                    "source_type_id": "aws",
                    "availability_status": "available"
                }
            }

            response = requests.post('https://console.redhat.com/api/sources/v3.1/sources',
                                     auth=(USER, PASSWORD), json=source_data)
            if response.status_code != 201:
                print(f"Failed to create source for {name}")
            else:
                print(f"Source created for {name}")

except FileNotFoundError:
    print(f"{INPUT} not found")
    exit(1)
