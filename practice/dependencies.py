from database import get_connection

# it tells api to connect endpoint auto when request comes (dependency wrapper)
def get_db():
   # """function that connect endpoints to database automatically"""
    conn = get_connection()
    try:
        yield conn # return connection and wait until request ends
    
    finally:
        conn.close()