from flask import make_response, jsonify, request
from flask_restful import Resource

from models import ATM
from utils import authenticate, database


def helper(capability, activity):
    return capability == "SUPPORTED" and activity == "AVAILABLE"


class ATMsResource(Resource):

    @authenticate()
    def get(self, *args, **kwargs):
        atms = ATM.query.all()

        result = map(lambda x: x.serialize(), atms)
        return make_response(jsonify(dict(atms=list(result))), 200)

    @authenticate()
    def post(self, *args, **kwargs):
        data = request.json
        atms = data['atms']
        for atm_data in atms:
            new_atm = ATM(
                address=atm_data['address'],
                latitude=atm_data['latitude'],
                longitude=atm_data['longitude'],
                all_day=atm_data.get('all_day', False),

                wheelchair_service=helper(
                    capability=atm_data['services']['wheelchair']['serviceCapability'],
                    activity=atm_data['services']['wheelchair']['serviceActivity']
                ),
                blind_service=helper(
                    capability=atm_data['services']['blind']['serviceCapability'],
                    activity=atm_data['services']['blind']['serviceActivity']
                ),
                nfc_for_bank_cards_service=helper(
                    capability=atm_data['services']['nfcForBankCards']['serviceCapability'],
                    activity=atm_data['services']['nfcForBankCards']['serviceActivity']
                ),
                qr_read_service=helper(
                    capability=atm_data['services']['qrRead']['serviceCapability'],
                    activity=atm_data['services']['qrRead']['serviceActivity']
                ),
                supports_usd_service=helper(
                    capability=atm_data['services']['supportsUsd']['serviceCapability'],
                    activity=atm_data['services']['supportsUsd']['serviceActivity']
                ),
                supports_charge_rub_service=helper(
                    capability=atm_data['services']['supportsChargeRub']['serviceCapability'],
                    activity=atm_data['services']['supportsChargeRub']['serviceActivity']
                ),
                supports_eur_service=helper(
                    capability=atm_data['services']['supportsEur']['serviceCapability'],
                    activity=atm_data['services']['supportsEur']['serviceActivity']
                ),
                supports_rub_service=helper(
                    capability=atm_data['services']['supportsRub']['serviceCapability'],
                    activity=atm_data['services']['supportsRub']['serviceActivity']
                ),

            )
            database.session.add(new_atm)
        database.session.commit()
        return make_response(jsonify({'message': 'Added all ATMs to the database'}), 200)
