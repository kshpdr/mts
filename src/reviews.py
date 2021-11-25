#import local_configs as config
import env_configs as config
import psycopg2

conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
cur = conn.cursor()


def save_review_database(module_id, review, module_name):
    cur.execute(f"INSERT INTO reviews (module_id, review, module_name) \
                VALUES ({module_id}, '{review}', '{module_name}')")
    conn.commit()


def save_star_database(module_id, module_name, star, user_id):
    cur.execute(f"SELECT module_id, user_id, star FROM stars \
                WHERE module_id = {module_id} AND user_id = {user_id}")
    row = cur.fetchone()
    print(row)
    if row is not None:
        conn.commit()
        return "fail"
    else:
        cur.execute(f"INSERT INTO stars (module_id, module_name, star, user_id) \
                    VALUES ({module_id}, '{module_name}', {star}, {user_id})")
        conn.commit()
        return "success"



def get_all_reviews(module_id, module_name):
    all_reviews = ""
    cur.execute(f"SELECT * FROM reviews \
                WHERE module_id = {module_id}")
    row = cur.fetchone()
    if row is None:
        all_reviews += "Leider gibt es jetzt keine Rezensionen für dieses Modul. Aber du kannst eine hinzufügen!"
        return all_reviews
    all_reviews = f"<b>Alle Rezensionen für {module_name}:</b>\n\n"
    while row is not None:
        all_reviews += "• "
        all_reviews += row[1]
        all_reviews += "\n \n"
        row = cur.fetchone()
    conn.commit()
    return all_reviews


def reviews_in_total():
    cur.execute("SELECT COUNT(*) FROM reviews")
    row = cur.fetchone()
    return row[0]


def modules_in_total():
    cur.execute("SELECT COUNT(DISTINCT module_id) FROM reviews")
    row = cur.fetchone()
    return row[0]


def reviewed_modules():
    modules = "*Diese Module wurden schon bewertet:*\n\n"
    cur.execute("SELECT DISTINCT module_name FROM reviews")
    row = cur.fetchone()
    while row is not None:
        modules += "• "
        modules += row[0]
        modules += "\n"
        row = cur.fetchone()
    conn.commit()
    return modules


def calculate_average_star(module_id):
    cur.execute(f"SELECT {module_id} FROM stars")
    row = cur.fetchone()
    if row is None:
        conn.commit()
        return None
    else:
        cur.execute(f"SELECT AVG(star) FROM stars \
                    WHERE module_id = {module_id}")
        average_star = cur.fetchone()[0]
        conn.commit()
        return average_star