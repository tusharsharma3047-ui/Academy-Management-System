import sqlite3

conn = sqlite3.connect("data/academy.db", timeout= 10)
cursor = conn.cursor()



# Salary table
cursor.execute("""
ALTER TABLE fees
ADD COLUMN fee_month TEXT;


""")

conn.commit()
conn.close()

print("Faculty and salary tables created")
