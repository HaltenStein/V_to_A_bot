import sqlite3


class SQL:
    conn = sqlite3.connect("data_bot.db")

    @classmethod
    def create_db(cls) -> None:
        cursor = cls.conn.cursor()
        try:
            cursor.execute("""CREATE TABLE DataAudio(
                id_audio     TEXT    PRIMARY KEY NOT NULL,
                name_audio   TEXT    NOT NULL,
                performer    STRING  NOT NULL,
                length_audio INTEGER NOT NULL,
                format       STRING  NOT NULL);""")
            cursor.execute("""CREATE TABLE User(
                id              INTEGER      PRIMARY KEY NOT NULL,
                count_downloads INTEGER,
                prime_version   BOOLEAN,
                date_bay_prime  DATA,
                language        VARCHAR (30));""")
        except:
            pass
        cls.conn.commit()
        cursor.close()

    @classmethod
    def db_check_audio(cls, name_audio: str, length: int, author: str, quality: str) -> str:
        """
        Check audio in users.db
        """
        cursor = cls.conn.cursor()  
        params = (name_audio, length, author, quality)
        try:
            cursor.execute("""SELECT id_audio FROM DataAudio WHERE
                name_audio=? AND length_audio=?
                and performer=? AND format=?;""", (params))
            id_audio = cursor.fetchall()
            cursor.close()
            return id_audio
        except sqlite3.DatabaseError as err:       
            print("Error:", err)

    @classmethod
    def db_insert_audio(cls, id_audio: str, name_audio: str,
                            author: str, length: int, quality: str) -> None:
        """
        Adding audio data to the database
        """
        cursor = cls.conn.cursor()
        params = (id_audio, name_audio, length, author, quality)
        try:
            cursor.execute("""INSERT INTO DataAudio (id_audio, name_audio, performer,
                            length_audio, format) VALUES (?, ?, ?, ?, ?);""", (params))
            cls.conn.commit()
            cursor.close()
        except sqlite3.DatabaseError as err:       
            print("Error:", err)

    @classmethod
    def db_select_id(cls, id: int):
        """check user in users.db:\n
            -adding its id if it's not there\n
            or\n-number of downloaded files +1
        """
        cursor = cls.conn.cursor()
        try:
            cursor.execute("SELECT id FROM User WHERE id = ?;", (id, ))
            request = cursor.fetchall()

            if 0 == len(request):  # if new user
                cursor.execute("INSERT INTO User (id, count_downloads) VALUES (?, 1);", (id, ))
            else:  # download counter + 1
                cursor.execute("""UPDATE User SET count_downloads =
                                    count_downloads + 1 WHERE id = ?;""", (id, ))
            cls.conn.commit()
            cursor.close()
        except sqlite3.DatabaseError as err:     
            print("Error:", err)

    @classmethod
    def select_prime_user(cls) -> list():
        cursor = cls.conn.cursor()
        try:
            cursor.execute("SELECT id FROM User WHERE prime_version = True;")
            list_prime_id = cursor.fetchall()
            cursor.close()
            return list_prime_id
        except sqlite3.DatabaseError as err:
            print("Error:", err)

    @classmethod
    def add_prime_user(cls, id: int):
        cursor = cls.conn.cursor()
        try:
            cursor.execute("UPDATE User SET prime_version = True WHERE id = '?'", (id, ))
            cursor.close()
        except sqlite3.DatabaseError as err:
            print("Error:", err)

    def close_connect(cls):
        cls.conn.close()
