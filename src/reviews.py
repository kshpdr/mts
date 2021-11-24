# import local_configs as config
import env_configs as config
import psycopg2

conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
cur = conn.cursor()


def save_review_database(module_id, review, module_name):
    cur.execute(f"INSERT INTO reviews (module_id, review, module_name) \
                VALUES ({module_id}, '{review}', '{module_name}')")
    conn.commit()


def get_all_reviews(module_id, module_name):
    all_reviews = f"<b>Alle Bewertungen für {module_name}:</b>\n\n"
    cur.execute(f"SELECT * FROM reviews \
                WHERE module_id = {module_id}")
    row = cur.fetchone()
    if row is None:
        return "Leider gibt es jetzt keine Bewertungen für dieses Modul. Aber du kannst eine hinzufügen!"
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