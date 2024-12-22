from load_data.service import read_from_csv, insert_region, insert_country, insert_city, insert_target_type, \
    insert_attack_type, insert_group, insert_event
from api_queries.postgres_db.connect import session_maker
CSV_PATH_EXM = "../data/globalterroris-1000 rows.csv"
CSV_PATH = "../data/globalterrorismdb.csv"


def init_db():
    data = read_from_csv(CSV_PATH)
    if data is None:
        print("No data")
        return
    session = session_maker()
    for row in data:
        region_id = insert_region(session, row)
        country_id = insert_country(session, row, region_id)
        city_id = insert_city(session,row, country_id)
        target_type_id = insert_target_type(session, row)
        attack_type_id = insert_attack_type(session, row)
        group_id = insert_group(session, row)
        insert_event(session, row, city_id, attack_type_id, target_type_id, group_id)


    session.close()





init_db()
