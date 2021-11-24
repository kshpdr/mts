import local_configs as config
# import env_configs as config
import psycopg2

conn = psycopg2.connect(config.database_url, sslmode='require')
cur = conn.cursor()


def save_review_database(module_id, review):
    cur.execute(f"INSERT INTO reviews (module_id, review) \
                VALUES ({module_id}, '{review}')")
    conn.commit()


def get_all_reviews(module_id):
    all_reviews = ""
    cur.execute(f"SELECT * FROM reviews \
                WHERE module_id = {module_id}")
    row = cur.fetchone()
    if row is None:
        return "Leider gibt es jetzt keine Bewertungen für dieses Modul. Aber du kannst eine hinzufügen!"
    while row is not None:
        all_reviews += row[1]
        all_reviews += "\n \n"
        row = cur.fetchone()
    conn.commit()
    return all_reviews