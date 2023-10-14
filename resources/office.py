import random
from datetime import datetime

from flask import make_response, jsonify, request
from flask_restful import Resource

from models import Office, OpenHour, DailyLoad
from utils import authenticate, database

days = {
    "пн-пт": [0, 1, 2, 3, 4],
    "пн-чт": [0, 1, 2, 3],
    "пн": [0],
    "вт": [1],
    "ср": [2],
    "чт": [3],
    "пт": [4],
    "сб": [5],
    "вс": [6],
    "сб,вс": [5, 6],
}


def helper(day, hours, office_id, is_individual, session):
    start, end = hours.split('-')
    start = int(start.split(":")[0])
    end = int(end.split(":")[0])

    load = []
    for _ in range(start, end):
        load.append(str(random.randint(0, 100)))

    days_of_week = days.get(day) or []
    for day in days_of_week:
        new_daily_load = DailyLoad(
            office_id=office_id,
            day_of_week=day,
            is_individual=is_individual,
            load_level=', '.join(load),
        )
        session.add(new_daily_load)


def get_loads(loads_dict, key):
    if loads_dict == {}:
        return None
    loads = loads_dict.get(key)
    if loads:
        return loads.split(', ')
    return None

class OfficesResource(Resource):

    @authenticate()
    def get(self, *args, **kwargs):
        offices = Office.query.all()
        open_hours = OpenHour.query.all()
        weekday = datetime.today().weekday()
        daily_loads = DailyLoad.query.filter_by(day_of_week=str(weekday)).all()

        loads_dict = {}
        for load in daily_loads:
            if load.office_id in loads_dict:
                if load.is_individual:
                    loads_dict[load.office_id]['loads_individual'] = load.load_level
                else:
                    loads_dict[load.office_id]['loads'] = load.load_level
            else:
                if load.is_individual:
                    loads_dict[load.office_id] = {'loads_individual': load.load_level}
                else:
                    loads_dict[load.office_id] = {'loads': load.load_level}

        result_dict = {}
        result_individual_dict = {}
        for open_hour in open_hours:
            if open_hour.is_individual:
                if open_hour.office_id in result_individual_dict:
                    result_individual_dict[open_hour.office_id].append(open_hour.serialize())
                else:
                    result_individual_dict[open_hour.office_id] = [open_hour.serialize()]
            else:
                if open_hour.office_id in result_dict:
                    result_dict[open_hour.office_id].append(open_hour.serialize())
                else:
                    result_dict[open_hour.office_id] = [open_hour.serialize()]

        result = map(lambda x: {
            **x.serialize(),
            "open_hours": result_dict.get(x.id, []),
            "openHoursIndividual": result_individual_dict.get(x.id, []),
            "loads_individual": get_loads(loads_dict.get(x.id, {}), 'loads_individual'),
            "loads": get_loads(loads_dict.get(x.id, {}), 'loads')}, offices)

        return make_response(jsonify(dict(offices=list(result))), 200)

    @authenticate()
    def post(self, *args, **kwargs):
        data = request.json
        session = database.session

        for entry in data:
            new_office = Office(
                name=entry['salePointName'],
                address=entry['address'],
                status=entry['status'],
                rko=entry.get('rko') or False,
                office_type=entry['officeType'],
                sale_point_format=entry['salePointFormat'],
                suo_availability=entry.get('suoAvailability') or False,
                has_ramp=entry.get('hasRamp') or False,
                latitude=entry['latitude'],
                longitude=entry['longitude'],
                metro_station=entry['metroStation'],
                kep=entry.get('kep') or False,
                my_branch=entry['myBranch'],
            )
            session.add(new_office)
            session.flush()

            for open_hour in entry['openHours']:
                if open_hour.get('days') != "Не обслуживает ЮЛ":
                    if open_hour.get('hours') != "выходной":
                        helper(
                            day=open_hour['days'],
                            hours=open_hour.get('hours'),
                            office_id=new_office.id,
                            is_individual=False,
                            session=session
                        )
                    new_open_hour = OpenHour(
                        office_id=new_office.id,
                        day_of_week=open_hour['days'],
                        hours=open_hour.get('hours') or 'не обслуживает ЮЛ',
                        is_individual=False,
                    )
                    session.add(new_open_hour)

            for open_hour_individual in entry['openHoursIndividual']:
                if open_hour_individual.get('days') != "Не обслуживает ФЛ":
                    if open_hour_individual.get('hours') != "выходной":
                        helper(
                            day=open_hour_individual['days'],
                            hours=open_hour_individual.get('hours'),
                            office_id=new_office.id,
                            is_individual=True,
                            session=session
                        )
                    new_open_hour_individual = OpenHour(
                        office_id=new_office.id,
                        day_of_week=open_hour_individual['days'],
                        hours=open_hour_individual.get('hours') or 'не обслуживает ФЛ',
                        is_individual=True,
                    )
                    session.add(new_open_hour_individual)

        session.commit()
        return make_response(jsonify({'message': 'Added all Offices to the database'}), 200)
