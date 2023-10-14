from flask import make_response, jsonify, request
from flask_restful import Resource

from models import Office, OpenHour
from utils import authenticate, database


class OfficesResource(Resource):

    @authenticate()
    def get(self, *args, **kwargs):
        offices = Office.query.all()
        open_hours = OpenHour.query.all()

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
            "openHoursIndividual": result_individual_dict.get(x.id, [])},
                     offices)

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
                    new_open_hour = OpenHour(
                        office_id=new_office.id,
                        day_of_week=open_hour['days'],
                        hours=open_hour.get('hours') or 'не обслуживает ЮЛ',
                        is_individual=False,
                    )
                    session.add(new_open_hour)

            for open_hour_individual in entry['openHoursIndividual']:
                if open_hour_individual.get('days') != "Не обслуживает ФЛ":
                    new_open_hour_individual = OpenHour(
                        office_id=new_office.id,
                        day_of_week=open_hour_individual['days'],
                        hours=open_hour_individual.get('hours') or 'не обслуживает ФЛ',
                        is_individual=True,
                    )
                    session.add(new_open_hour_individual)

        session.commit()
        return make_response(jsonify({'message': 'Added all Offices to the database'}), 200)
