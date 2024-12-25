import csv
from datetime import datetime

from load.postgres_db.connect import engine, session_maker
from load.postgres_db.models.event_model import Event

from load.postgres_db.models.country_model import Country
from load.postgres_db.models.city_model import City
from load.postgres_db.models.group_model import Group
from load.postgres_db.models.attack_type_model import AttackType
CSV_PATH = "data/RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv"



def read_from_csv(file_path):
    try:
        with open(file_path, 'r', encoding='latin1') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return None

def parse_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d-%b-%y")
        return {
            'year': parsed_date.year,
            'month': parsed_date.month,
            'day': parsed_date.day
        }
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return {'year': None, 'month': None, 'day': None}
def get_or_insert_group(session, group_name):
    group = session.query(Group).filter(Group.name == group_name).first()
    if group:
        return group.id
    else:
        new_group = Group(name=group_name)
        session.add(new_group)
        session.commit()
        session.refresh(new_group)
        return new_group.id

def get_or_insert_country(session, country_name):
    country_name = country_name.strip().lower() if country_name else ""
    country = session.query(Country).filter(Country.name == country_name).first()
    if country:
        return country.id
    elif country_name:
        new_country = Country(name=country_name)
        session.add(new_country)
        session.commit()
        session.refresh(new_country)
        return new_country.id
    return None

def get_or_insert_city(session, city_name, country_name):
    city = session.query(City).filter(City.name == city_name).first()
    if city:
        return city.id
    else:
        country_id = get_or_insert_country(session, country_name)  # חפש או צור את המדינה
        if not country_id:  # אם לא נמצא country_id, לא ניצור עיר
            print(f"Country '{country_name}' not found. Skipping city creation.")
            return None
        new_city = City(name=city_name, country_id=country_id)  # עכשיו יש לך country_id תקני
        session.add(new_city)
        session.commit()
        session.refresh(new_city)
        return new_city.id


def get_or_insert_attack_type(session, attack_type_name):
    attack_type_name = attack_type_name.strip().lower()
    attack_type = session.query(AttackType).filter(AttackType.name == attack_type_name).first()
    if attack_type:
        return attack_type.id
    elif attack_type_name:
        new_attack_type = AttackType(name=attack_type_name)
        session.add(new_attack_type)
        session.commit()
        session.flush()
        session.refresh(new_attack_type)
        return new_attack_type.id
    return None

def parse_event_data(session, row):
    try:
        date_parts = parse_date(row.get('Date', ''))
        group_id = get_or_insert_group(session, row.get('Perpetrator')) if row.get('Perpetrator') else None
        city_id = get_or_insert_city(session, row.get('City'), row.get('Country')) if row.get('City') else None
        attack_type_id = get_or_insert_attack_type(session, row.get('Weapon')) if row.get('Weapon') else None

        return Event(
            year=date_parts['year'],
            month=date_parts['month'],
            day=date_parts['day'],
            city_id=city_id,
            summary=row.get('Description'),
            killed=int(row['Fatalities']) if row['Fatalities'] else 0,
            wounded=int(row['Injuries']) if row['Injuries'] else 0,
            group_id=group_id,
            attack_type_id=attack_type_id
        )
    except Exception as e:
        print(f"Error parsing row {row}: {e}")
        return None

def insert_data():
    data = read_from_csv(CSV_PATH)
    if data is None:
        return
    try:
        session = session_maker()
        for row in data:
            event = parse_event_data(session, row)
            if event:
                session.add(event)

        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while inserting data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_data()
# SELECT setval(pg_get_serial_sequence('countries', 'id'), (SELECT MAX(id) FROM countries));
#SELECT setval(pg_get_serial_sequence('attack_types', 'id'), (SELECT MAX(id) FROM attack_types));

