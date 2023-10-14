from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean

from utils import database


class ATM(database.Model):
    __tablename__ = 'atms'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    all_day = Column(Boolean, nullable=False)
    wheelchair_service = Column(Boolean, nullable=False)
    blind_service = Column(Boolean, nullable=False)
    nfc_for_bank_cards_service = Column(Boolean, nullable=False)
    qr_read_service = Column(Boolean, nullable=False)
    supports_usd_service = Column(Boolean, nullable=False)
    supports_charge_rub_service = Column(Boolean, nullable=False)
    supports_eur_service = Column(Boolean, nullable=False)
    supports_rub_service = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'all_day': self.all_day,
            'wheelchair_service': self.wheelchair_service,
            'blind_service': self.blind_service,
            'nfc_for_bank_cards_service': self.nfc_for_bank_cards_service,
            'qr_read_service': self.qr_read_service,
            'supports_usd_service': self.supports_usd_service,
            'supports_charge_rub_service': self.supports_charge_rub_service,
            'supports_eur_service': self.supports_eur_service,
            'supports_rub_service': self.supports_rub_service,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
