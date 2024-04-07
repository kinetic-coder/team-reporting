import requests
import pyodbc
import Utilities.Settings as Settings

def recordExists(cursor, table, column, value):
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = ?", value)
    return cursor.fetchone() is not None

def executeQuery(cursor, query):
    cursor.execute(query)

def getAllIssues(cursor):
    
    cursor.execute("SELECT * FROM Issue")
    rows = cursor.fetchall()

    # Create a dictionary to store the rows
    issues_dict = {}

    # Loop through the rows and add them to the dictionary
    for row in rows:
        # Assuming the 'Key' column is the first column in the row
        issues_dict[row[0]] = row[1:]

    return issues_dict

# Now you can use the secrets dictionary to access your secrets
settings = Settings.get_settings('settings/secrets.json')

# Define Jira API endpoint and JQL query
jira_url = settings["jira-url"]

jql_query = settings["jira-query"]

bearer_setting = f"Bearer {settings['jira-pak']}"

# Initialize startAt and maxResults
start_at = 0
max_results = 50  # Adjust this value as needed

data_to_insert = []

while True:
    # Send a GET request to the Jira API
    response = requests.get(
        jira_url,
        params={"jql": jql_query, "startAt": start_at, "maxResults": max_results},
        headers={"Authorization": bearer_setting, "Content-Type": "application/json"},
    )

    # Parse the response to get the desired data
    issues = response.json()["issues"]
    data_to_insert.extend([(issue["key"], issue["fields"]["summary"], issue["fields"]["status"]["name"]) for issue in issues])

    # If the number of issues in the response is less than maxResults, we've retrieved all issues
    if len(issues) < max_results:
        break

    # Otherwise, increment startAt by maxResults for the next iteration
    start_at += max_results

# Connect to the SQL Server database
conn = pyodbc.connect(settings['sql-connection-string'])

# Create a cursor
cursor = conn.cursor()

existingRecords = getAllIssues(cursor)
print(f"There are currently {len(existingRecords)} existingRecords)")

insertSQL = """INSERT INTO Issue ([key], [Summary], [Status]) VALUES (?, ?, ?)"""
updateSQL = """UPDATE Issue SET [Summary] = ?, [Status] = ? WHERE [key] = ?"""

print("Storing data from Jira in the database...")
print(f"{len(data_to_insert)} records to insert/update")
for data in data_to_insert:
    primaryKey = data[0]

    if(len(existingRecords) == 0 or primaryKey not in existingRecords):
        cursor.execute(insertSQL, (data[0], data[1], data[2]))
    else:
        cursor.execute(updateSQL, (data[1], data[2], data[0]))

print("Comitting changes...")
cursor.commit()

print("Closing connection...")
cursor.close()