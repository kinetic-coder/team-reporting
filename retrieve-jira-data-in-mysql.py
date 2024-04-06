import requests
import mysql.connector
import json
import Utilities.Settings as Settings

# Now you can use the secrets dictionary to access your secrets
settings = Settings.get_settings('settings/secrets.json')

# Define Jira API endpoint and JQL query
jira_url = settings["jira-url"]

jql_query = settings["jira-query"]

bearer_setting = f"Bearer {settings['jira-pak']}"

# Send a GET request to the Jira API
response = requests.get(
    jira_url,
    params={"jql": jql_query},
    headers={"Authorization": bearer_setting, "Content-Type": "application/json"},
)

# Parse the response to get the desired data
issues = response.json()["issues"]
data_to_insert = [(issue["key"], issue["fields"]["labels"]) for issue in issues]

# Connect to the MySQL database
db = mysql.connector.connect(
    host=settings["database-host"],
    user=settings["database-user"],
    password=settings["database-password"],
    database=settings["database-name"],
)

# Create database if it does not exist...
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS jira")
cursor.execute(f"USE {settings['database-name']}")

# Create a table (if not exists) to store the data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Issues (
        key VARCHAR(255),
        labels VARCHAR(255)
    )
""")

# Insert the data into the table
for data in data_to_insert:
    cursor.execute("INSERT INTO Issues (key, labels) VALUES (%s, %s)", data)

# Commit the changes and close the connection
db.commit()
db.close()