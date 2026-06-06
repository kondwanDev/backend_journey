import psycopg

conn = psycopg.connect (
    host = "localhost",
    dbname = "book_api",
    user = "postgres",
    password = "malone265"
)

cur = conn.cursor () #cursor is sql commands executor, conn ->inside db systems

cur.execute(
    """
    INSERT INTO books (title,author,year)
    VALUES (%s, %s, %s)
    """,
    ("the trial","Franz Kafka",1992)
)

conn.commit() #save changes

print ("Book insert successfully!")

cur.close() # stop cursor
conn.close() # close connection