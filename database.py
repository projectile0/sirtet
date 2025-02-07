# Функция для вставки нового результата в базу данных
def insert_score(conn, nickname, score):
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (nickname, score) VALUES (?, ?)", (nickname, score))
    conn.commit()

# Функция для получения топ-10 результатов
def get_top_scores(conn):
    cur = conn.cursor()
    cur.execute("SELECT nickname, score FROM scores ORDER BY score DESC LIMIT 10")
    return cur.fetchall()