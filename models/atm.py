from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean

from utils import database


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
            'services': [
                dict(name='wheelchair_service', capability=self.wheelchair_service_capability, activity=self.wheelchair_service_activity),
                dict(name='blind_service', capability=self.blind_service_capability, activity=self.blind_service_activity),
                dict(name='nfc_for_bank_cards_service', capability=self.nfc_for_bank_cards_service_capability, activity=self.nfc_for_bank_cards_service_activity),
                dict(name='qr_read_service', capability=self.qr_read_service_capability, activity=self.qr_read_service_activity),
                dict(name='supports_usd_service', capability=self.supports_usd_service_capability, activity=self.supports_usd_service_activity),
                dict(name='supports_charge_rub_service', capability=self.supports_charge_rub_service_capability, activity=self.supports_charge_rub_service_activity),
                dict(name='supports_eur_service', capability=self.supports_eur_service_capability, activity=self.supports_eur_service_activity),
                dict(name='supports_rub_service', capability=self.supports_rub_service_capability, activity=self.supports_rub_service_activity),
            ],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
