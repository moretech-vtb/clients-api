from flask import make_response, jsonify, request
from flask_restful import Resource

from models import Office, OpenHour
from utils import authenticate, database


class OfficesResource(Resource):

    @authenticate()
    def post(self, *args, **kwargs):
        data = request.json
        session = database.session

        for entry in data:
            new_office = Office(
                name=entry['salePointName'],
                address=entry['address'],
                status=entry['status'],
                rko=entry['rko'],
                office_type=entry['officeType'],
                sale_point_format=entry['salePointFormat'],
                suo_availability=entry['suoAvailability'],
                has_ramp=entry['hasRamp'],
                latitude=entry['latitude'],
                longitude=entry['longitude'],
                metro_station=entry['metroStation'],
                distance=entry['distance'],
                kep=entry['kep'],
                my_branch=entry['myBranch'],

            )
            session.add(new_office)
            session.flush()

            for open_hour in entry['openHours']:
                new_open_hour = OpenHour(
                    office_id=new_office.id,
                    day_of_week=open_hour['days'],
                    hours=open_hour.get('hours') or 'не обслуживает ЮЛ',
                    is_individual=False,
                )
                session.add(new_open_hour)

            for open_hour_individual in entry['openHoursIndividual']:
                new_open_hour_individual = OpenHour(
                    office_id=new_office.id,
                    day_of_week=open_hour_individual['days'],
                    hours=open_hour_individual.get('hours') or 'не обслуживает ФЛ',
                    is_individual=True,
                )
                session.add(new_open_hour_individual)

        session.commit()
        return make_response(jsonify({'message': 'Added all ATMs to the database'}), 200)
