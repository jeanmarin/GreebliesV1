import sqlite3

# Connect to the database
conn = sqlite3.connect('organism_data.db')

# Create a cursor object to execute queries
c = conn.cursor()

# Execute a query to select all rows from the organisms table
c.execute('SELECT * FROM organisms')

# Fetch all the rows and print them out
rows = c.fetchall()
for row in rows:
    print(row)

# Close the cursor and database connection
c.close()
conn.close()