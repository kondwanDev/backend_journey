from psycopg.rows import dict_row

class UserRepository:

    @staticmethod
    def get_user_by_email (conn, email:str):
       
       cur = conn.cursor (row_factory = dict_row)
       cur.execute ("""
                    SELECT * FROM users WHERE email = %s
                 """,(email,))
       
       existing_user = cur.fetchone ()

       cur.close ()
       return existing_user
    
    @staticmethod
    def get_user_by_name (conn, username:str):

        cur = conn.cursor (row_factory = dict_row)
        cur.execute ("""
                     SELECT * FROM users WHERE username = %s
                 """, (username,))
        
        existing_username = cur.fetchone()
        cur.close()

        return existing_username

    @staticmethod
    def create_user (conn, username: str, email:str, password_hash:str):

        cur =conn.cursor (row_factory = dict_row)
        cur.execute ("""
                     INSERT INTO users (username, email, password_hash)
                     VALUES (%s,%s,%s)
                     RETURNING id, username, email, created_at""",
                     (username, email, password_hash))
        
        user = cur.fetchone()

        conn.commit()
        cur. close()

        return user