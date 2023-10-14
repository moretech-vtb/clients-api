from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean

from utils import database


def helper(capability, activity):
    return capability == "SUPPORTED" and activity == "AVAILABLE"


class ATM(database.Model):
    __tablename__ = 'atms'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    all_day = Column(Boolean, nullable=False)
    wheelchair_service_capability = Column(String)
    wheelchair_service_activity = Column(String)
    blind_service_capability = Column(String)
    blind_service_activity = Column(String)
    nfc_for_bank_cards_service_capability = Column(String)
    nfc_for_bank_cards_service_activity = Column(String)
    qr_read_service_capability = Column(String)
    qr_read_service_activity = Column(String)
    supports_usd_service_capability = Column(String)
    supports_usd_service_activity = Column(String)
    supports_charge_rub_service_capability = Column(String)
    supports_charge_rub_service_activity = Column(String)
    supports_eur_service_capability = Column(String)
    supports_eur_service_activity = Column(String)
    supports_rub_service_capability = Column(String)
    supports_rub_service_activity = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'all_day': self.all_day,
            'wheelchair_service': helper(capability=self.wheelchair_service_capability,
                                         activity=self.wheelchair_service_activity),
            'blind_service': helper(capability=self.blind_service_capability,
                                    activity=self.blind_service_activity),
            'nfc_for_bank_cards_service': helper(capability=self.nfc_for_bank_cards_service_capability,
                                                 activity=self.nfc_for_bank_cards_service_activity),
            'qr_read_service': helper(capability=self.qr_read_service_capability,
                                      activity=self.qr_read_service_activity),
            'supports_usd_service': helper(capability=self.supports_usd_service_capability,
                                           activity=self.supports_usd_service_activity),
            'supports_charge_rub_service': helper(capability=self.supports_charge_rub_service_capability,
                                                  activity=self.supports_charge_rub_service_activity),
            'supports_eur_service': helper(capability=self.supports_eur_service_capability,
                                           activity=self.supports_eur_service_activity),
            'supports_rub_service': helper(capability=self.supports_rub_service_capability,
                                           activity=self.supports_rub_service_activity),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
