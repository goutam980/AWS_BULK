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
    name = "John Doe"
    aws_access_key_id = "YOUR_AWS_ACCESS_KEY_ID"
    aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"

    with open(INPUT, 'r') as csvfile:
      reader = csv.reader(csvfile)
      header = next(reader)  # Read the header row
      for row in reader:
        if row:  # Check if the row is not empty
           if len(row) >= 3:  # Ensure the row has at least 3 elements
              row[0] = name
              row[1] = aws_access_key_id
              row[2] = aws_secret_access_key
              source_data = {
                  "source": {
                      "name": name,
                      "access_key_id": aws_access_key_id,
                      "secret_access_key": aws_secret_access_key,
                      "source_type_id": "aws",
                      "availability_status": "available"
                  }
              }
              print(source_data)

           else:
              print("Invalid row:", row)
        else:
          print("Empty row encountered")
        response = requests.post('https://console.redhat.com/api/sources/v3.1/sources', auth=(USER, PASSWORD), json=source_data)
        if response.status_code != 201:
            print(f"Failed to create source for {name}")
        else:
            print(f"Source created for {name}")

except FileNotFoundError:
    print(f"{INPUT} not found")
    exit(1)
