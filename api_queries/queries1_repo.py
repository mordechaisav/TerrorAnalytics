from sqlalchemy import func, desc, distinct
from api_queries.postgres_db.connect import session_maker
from api_queries.postgres_db.models import AttackType, TargetType
from api_queries.postgres_db.models.city_model import City
from api_queries.postgres_db.models.country_model import Country

from api_queries.postgres_db.models.event_model import Event
from api_queries.postgres_db.models.group_model import Group
from api_queries.postgres_db.models.region_model import Region

session = session_maker()
def get_top_attack_types(top_n=None):
    query = (
        session.query(
            AttackType.name,
            func.sum(Event.killed * 2 + Event.wounded).label("total_score")
        )
        .join(Event.attack_type)
        .group_by(AttackType.name)
        .order_by(desc("total_score"))
    )
    if top_n:
        query = query.limit(top_n)

    return query.all()





def regions_with_severity(limit=5):
    weighted_avg_by_region = session.query(
        Region.name.label('region_name'),
        func.avg(Event.killed * 2 + Event.wounded).label('severity_score')

    ) \
        .join(Country, Region.id == Country.region_id) \
        .join(City, Country.id == City.country_id) \
        .join(Event, City.id == Event.city_id) \
        .group_by(Region.name) \
        .having(func.avg(Event.killed * 2 + Event.wounded).isnot(None)) \
        .order_by(func.avg(Event.killed * 2 + Event.wounded).desc()) \
        .limit(limit) \
        .all()
    return weighted_avg_by_region



def group_with_most_casualties():
    top_groups = session.query(
        Group.name.label('group_name'),
        func.sum(Event.killed + Event.wounded).label('total_casualties')
    ) \
       .join(Group, Event.group_id == Group.id) \
       .group_by(Group.name) \
       .having(func.sum(Event.killed + Event.wounded).isnot(None)) \
       .order_by(desc('total_casualties')) \
       .limit(5) \
       .all()
    return top_groups



def max_difference_between_consecutive_years_with_percentage():
    events_by_year_and_region = session.query(
        Region.name.label('region_name'),
        Event.year.label('year'),
        func.count(Event.id).label('total_events')
    ) \
        .join(Country, Region.id == Country.region_id) \
        .join(City, Country.id == City.country_id) \
        .join(Event, City.id == Event.city_id) \
        .group_by(Region.name, Event.year) \
        .order_by(Region.name, Event.year) \
        .all()

    region_differences = {}
    previous_year_events = {}

    for row in events_by_year_and_region:
        region_name = row.region_name
        year = row.year
        total_events = row.total_events

        if region_name in previous_year_events:
            prev_year, prev_events = previous_year_events[region_name]
            diff = abs(prev_events - total_events)

            if prev_events != 0:
                percentage_change = ((diff / prev_events) * 100)
            else:
                percentage_change = 0

            if region_name not in region_differences or percentage_change > region_differences[region_name]['percentage_change']:
                region_differences[region_name] = {
                    'year_with_max_change': f"{prev_year}-{year}",
                    'max_difference': diff,
                    'percentage_change': percentage_change
                }

        previous_year_events[region_name] = (year, total_events)

    sorted_region_differences = sorted(region_differences.items(), key=lambda x: x[1]['percentage_change'], reverse=True)

    return [
        {
            "region_name": region,
            "year_with_max_change": data['year_with_max_change'],
            "max_difference": data['max_difference'],
            "percentage_change": round(data['percentage_change'], 2)  # אחוז השינוי
        }
        for region, data in sorted_region_differences
    ]


def active_groups_by_region(region_name=None, limit=5):
    query = session.query(
        Group.name.label('group_name'),
        func.count(Event.id).label('event_count')
    ) \
        .join(Event, Group.id == Event.group_id) \
        .join(City, Event.city_id == City.id) \
        .join(Country, City.country_id == Country.id) \
        .join(Region, Country.region_id == Region.id)

    if region_name:
        query = query.filter(Region.name == region_name)

    active_groups = query.group_by(Group.name) \
        .order_by(func.count(Event.id).desc()) \
        .limit(limit) \
        .all()

    return active_groups


def groups_with_common_targets(region=None, country=None):
    query = session.query(
        Event.target_type_id.label('target_id'),
        func.count(Group.id).label('group_count'),
        Region.name.label('region_name'),
        Country.name.label('country_name'),
        func.array_agg(Group.name).label('group_names')
    ) \
    .join(Group, Event.group_id == Group.id) \
    .join(City, Event.city_id == City.id) \
    .join(Country, City.country_id == Country.id) \
    .join(Region, Country.region_id == Region.id) \
    .group_by(Event.target_type_id, Region.name, Country.name)
    if region:
        query = query.filter(Region.name == region)
    if country:
        query = query.filter(Country.name == country)
    results = query.order_by(func.count(Group.id).desc()).all()

    markers = []
    for result in results:
        markers.append({
            'region': result.region_name,
            'country': result.country_name,
            'target_id': result.target_id,
            'group_names': set(result.group_names),
            'group_count': len(set(result.group_names))
        })
    return markers

def regions_with_common_attack_strategies(region=None, country=None):
    query = session.query(
        AttackType.name.label('attack_type'),
        func.count(distinct(Group.id)).label('unique_groups_count'),
        Region.name.label('region_name'),
        Country.name.label('country_name'),
        func.array_agg(distinct(Group.name)).label('group_names')
    ) \
    .join(Event, AttackType.id == Event.attack_type_id) \
    .join(Group, Event.group_id == Group.id) \
    .join(City, Event.city_id == City.id) \
    .join(Country, City.country_id == Country.id) \
    .join(Region, Country.region_id == Region.id) \
    .group_by(AttackType.name, Region.name, Country.name)

    if region:
        query = query.filter(Region.name == region)
    if country:
        query = query.filter(Country.name == country)

    results = query.order_by(func.count(distinct(Group.id)).desc()).all()
    return [
        {
            'region': result.region_name,
            'country': result.country_name,
            'attack_type': result.attack_type,
            'unique_groups_count': result.unique_groups_count,
            'group_names': result.group_names
        }
        for result in results
    ]

def groups_with_similar_target_preferences():
    query = session.query(
        TargetType.name.label('target_type'),
        func.count(distinct(Group.id)).label('unique_groups_count'),
        func.array_agg(distinct(Group.name)).label('group_names')
    ) \
    .join(Event, TargetType.id == Event.target_type_id) \
    .join(Group, Event.group_id == Group.id) \
    .group_by(TargetType.name)

    results = query.order_by(func.count(distinct(Group.id)).desc()).all()
    return [
        {
            'target_type': result.target_type,
            'unique_groups_count': result.unique_groups_count,
            'group_names': result.group_names
        }
        for result in results
    ]

def regions_with_high_intergroup_activity(region=None):
    query = session.query(
        Region.name.label('region_name'),
        func.count(distinct(Group.id)).label('unique_groups_count'),
        func.array_agg(distinct(Group.name)).label('group_names')
    ) \
    .join(Event, Group.id == Event.group_id) \
    .join(City, Event.city_id == City.id) \
    .join(Country, City.country_id == Country.id) \
    .join(Region, Country.region_id == Region.id) \
    .group_by(Region.name)

    if region:
        query = query.filter(Region.name == region)

    results = query.order_by(func.count(distinct(Group.id)).desc()).all()
    return [
        {
            'region': result.region_name,
            'unique_groups_count': result.unique_groups_count,
            'group_names': result.group_names
        }
        for result in results
    ]





def groups_with_shared_targets_in_year(year):
    query = session.query(
        Event.target_type_id.label('target_id'),
        func.array_agg(distinct(Group.name)).label('group_names')
    ) \
    .join(Group, Event.group_id == Group.id) \
    .filter(Event.year == year) \
    .group_by(Event.target_type_id)

    results = query.all()
    return [
        {
            'target_id': result.target_id,
            'group_names': result.group_names
        }
        for result in results
    ]

