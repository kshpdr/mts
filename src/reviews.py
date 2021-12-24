#import local_configs as config
import env_configs as config
import psycopg2

conn = psycopg2.connect(config.DATABASE_URL, sslmode='require')
cur = conn.cursor()


def save_review_database(module_id, review, module_name, semester, user_id):
    try:
        cur.execute(f"INSERT INTO reviews (module_id, review, module_name, semester, user_id) \
                    VALUES ({module_id}, '{review}', '{module_name}', '{semester}', {user_id})")
        conn.commit()
        return True
    except:
        return False


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


def get_all_reviews_list(module_id, module_name):
    all_reviews = []
    cur.execute(f"SELECT * FROM reviews \
                WHERE module_id = {module_id}")
    row = cur.fetchone()
    if row is None:
        all_reviews = "Leider gibt es jetzt keine Rezensionen für dieses Modul. Aber du kannst eine hinzufügen!"
        return all_reviews
    while row is not None:
        all_reviews.append(row[1])
        row = cur.fetchone()
    conn.commit()
    return all_reviews


def get_all_semester_for_module(module_id, module_name):
    all_sems = []
    cur.execute(f"SELECT * FROM reviews \
                WHERE module_id = {module_id}")
    row = cur.fetchone()
    if row is None:
        all_sems = "Leider gibt es jetzt keine Rezensionen für dieses Modul. Aber du kannst eine hinzufügen!"
        return all_sems
    while row is not None:
        all_sems.append(row[3])
        row = cur.fetchone()
    conn.commit()
    return all_sems


def reviews_in_total():
    cur.execute("SELECT COUNT(*) FROM reviews")
    row = cur.fetchone()
    return row[0]


def modules_in_total():
    cur.execute("SELECT COUNT(DISTINCT module_id) FROM stars")
    row = cur.fetchone()
    print(row)
    return row[0]


def reviewed_modules():
    modules = "*Diese Module wurden schon kommentiert:*\n\n"
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