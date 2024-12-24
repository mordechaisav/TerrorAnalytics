import csv

from api_queries.postgres_db.models import AttackType
from api_queries.postgres_db.models.city_model import City
from api_queries.postgres_db.models.country_model import Country
from api_queries.postgres_db.models.event_model import Event
from api_queries.postgres_db.models.group_model import Group
from api_queries.postgres_db.models.region_model import Region
from api_queries.postgres_db.models import TargetType


def read_from_csv(file_path):
    try:
        with open(file_path, 'r',encoding='latin1') as file:

            reader = csv.DictReader(file)
            data = [row for row in reader]

            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return None


def insert_region(session, row):
    region_id = row.get('region')
    region_name = row.get("region_txt")
    if not region_name or not region_id:
        return
    try:
        check_region = session.query(Region).filter_by(id=region_id).first()
        if not check_region:
            new_region = Region(id=region_id, name=region_name)
            session.add(new_region)
            session.commit()
            session.refresh(new_region)
            return new_region.id
        else:
            return check_region.id
    except Exception as e:
        print(f"An error occurred while inserting the region: {str(e)}")

def insert_country(session,row, region_id):
    country_id = row.get('country')
    country = row.get('country_txt')
    try:
        check_country = session.query(Country).filter_by(id=country_id).first()
        if not check_country:
            new_country = Country(id=country_id, name=country, region_id=region_id)
            session.add(new_country)
            session.commit()
            session.refresh(new_country)
            return new_country.id
        else:
            return check_country.id
    except Exception as e:
        print(f"An error occurred while inserting the country: {str(e)}")

def insert_city(session,row, country_id):
    city = row.get('city')
    try:
        check_city = session.query(City).filter_by(name=city, country_id=country_id).first()
        if not check_city:
            new_city = City(name=city, country_id=country_id)
            session.add(new_city)
            session.commit()
            session.refresh(new_city)
            return new_city.id
        else:
            return check_city.id
    except Exception as e:
        print(f"An error occurred while inserting the city: {str(e)}")
def insert_target_type(session, row):
    target_type_id = row.get('targtype1')
    target_type = row.get('targtype1_txt')
    try:
        check_target = session.query(TargetType).filter_by(id=target_type_id).first()
        if not check_target:
            new_target = TargetType(id=target_type_id, name=target_type)
            session.add(new_target)
            session.commit()
            session.refresh(new_target)
            return new_target.id
        else:
            return check_target.id
    except Exception as e:
        print(f"An error occurred while inserting the target type: {str(e)}")

def insert_attack_type(session, row):
    attack_type_id = row.get('attacktype1')
    attack_type = row.get('attacktype1_txt')
    try:
        check_attack = session.query(AttackType).filter_by(id=attack_type_id).first()
        if not check_attack:
            new_attack = AttackType(id=attack_type_id, name=attack_type)
            session.add(new_attack)
            session.commit()
            session.refresh(new_attack)
            return new_attack.id
        else:
            return check_attack.id
    except Exception as e:
        print(f"An error occurred while inserting the attack type: {str(e)}")

def insert_group(session, row):
    group_name = row.get('gname')
    try:
        check_group = session.query(Group).filter_by(name=group_name).first()
        if not check_group:
            new_group = Group(name=group_name)
            session.add(new_group)
            session.commit()
            session.refresh(new_group)
            return new_group.id
        else:
            return check_group.id
    except Exception as e:
        print(f"An error occurred while inserting the group: {str(e)}")

def insert_event(session, row, city_id, attack_id, target_id, group_id):
    year = row.get('iyear')
    month = row.get('imonth')
    day = row.get('iday')
    latitude = row.get('latitude')
    longitude = row.get('longitude')
    summary = row.get('summary')
    killed = row.get('nkillus')
    wounded = row.get('nwound')

    # Validate and convert data types
    try:
        year = int(year) if year and year.isdigit() and 1900 <= int(year) <= 2025 else None
    except ValueError:
        year = None

    try:
        month = int(month) if month and month.isdigit() and 1 <= int(month) <= 12 else None
    except ValueError:
        month = None

    try:
        day = int(day) if day and day.isdigit() and 1 <= int(day) <= 31 else None
    except ValueError:
        day = None

    try:
        killed = int(killed) if killed and killed.isdigit() and int(killed) >= 0 else None
    except ValueError:
        killed = None

    try:
        wounded = int(wounded) if wounded and wounded.isdigit() and int(wounded) >= 0 else None
    except ValueError:
        wounded = None

    try:
        latitude = float(latitude) if latitude else None
    except ValueError:
        latitude = None

    try:
        longitude = float(longitude) if longitude else None
    except ValueError:
        longitude = None

    new_event = Event(
        year=year,
        month=month,
        day=day,
        latitude=latitude,
        longitude=longitude,
        summary=summary,
        killed=killed,
        wounded=wounded,
        city_id=city_id,
        attack_type_id=attack_id,
        target_type_id=target_id,
        group_id=group_id
    )
    try:
        session.add(new_event)
        session.commit()
        session.refresh(new_event)
        return new_event.id
    except Exception as e:
        print(f"An error occurred while inserting the event: {str(e)}")