from pydantic import BaseModel


class DonationBase(BaseModel):
    pass


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationBase):
    pass


class DonationDB(DonationBase):
    pass