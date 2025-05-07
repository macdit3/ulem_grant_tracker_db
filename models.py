# models.py
import os
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, Float, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This assumes 'app' is your FastAPI instance that's already defined

# Database Models
class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    donor_type = Column(String(20), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    organization_name = Column(String(200))
    email = Column(String(255))
    phone = Column(String(20))
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    preferred_contact_method = Column(String(20))
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donations = relationship("Donation", back_populates="donor")
    pledges = relationship("Pledge", back_populates="donor")
    thank_you_notes = relationship("ThankYouNote", back_populates="donor")


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(NUMERIC(10, 2))
    goal_amount = Column(NUMERIC(10, 2))
    current_progress = Column(NUMERIC(10, 2))
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donations = relationship("Donation", back_populates="program")
    pledges = relationship("Pledge", back_populates="program")


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    amount = Column(NUMERIC(10, 2), nullable=False)
    donation_date = Column(Date, nullable=False)
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    is_tax_deductible = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donor = relationship("Donor", back_populates="donations")
    program = relationship("Program", back_populates="donations")
    thank_you_notes = relationship("ThankYouNote", back_populates="donation")


class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    amount = Column(NUMERIC(10, 2), nullable=False)
    pledge_date = Column(Date, nullable=False)
    fulfillment_date = Column(Date)
    status = Column(String(50))
    amount_fulfilled = Column(NUMERIC(10, 2), nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donor = relationship("Donor", back_populates="pledges")
    program = relationship("Program", back_populates="pledges")


class TaxReceipt(Base):
    __tablename__ = "tax_receipts"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donations.id"))  # Note: This appears to be a FK to donations table, not donors
    year_donated = Column(Date)
    total_amount = Column(NUMERIC(10, 2), nullable=False)
    generated_date = Column(Date, nullable=False)
    sent_date = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donation = relationship("Donation")


class ThankYouNote(Base):
    __tablename__ = "thank_you_notes"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    donation_id = Column(Integer, ForeignKey("donations.id"))
    sent_date = Column(Date)
    method = Column(String(50))
    template_used = Column(String(100))
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    donor = relationship("Donor", back_populates="thank_you_notes")
    donation = relationship("Donation", back_populates="thank_you_notes")


# Pydantic Models for Request/Response
class DonorBase(BaseModel):
    donor_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    notes: Optional[str] = None


class DonorCreate(DonorBase):
    pass


class DonorResponse(DonorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    goal_amount: Optional[float] = None
    current_progress: Optional[float] = None


class ProgramCreate(ProgramBase):
    pass


class ProgramResponse(ProgramBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DonationBase(BaseModel):
    donor_id: int
    program_id: Optional[int] = None
    amount: float
    donation_date: date
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    is_tax_deductible: Optional[bool] = False
    notes: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationResponse(DonationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PledgeBase(BaseModel):
    donor_id: int
    program_id: Optional[int] = None
    amount: float
    pledge_date: date
    fulfillment_date: Optional[date] = None
    status: Optional[str] = None
    amount_fulfilled: float
    notes: Optional[str] = None


class PledgeCreate(PledgeBase):
    pass


class PledgeResponse(PledgeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaxReceiptBase(BaseModel):
    donor_id: int  # This represents the donation ID based on the SQL
    year_donated: Optional[date] = None
    total_amount: float
    generated_date: date
    sent_date: Optional[date] = None


class TaxReceiptCreate(TaxReceiptBase):
    pass


class TaxReceiptResponse(TaxReceiptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ThankYouNoteBase(BaseModel):
    donor_id: int
    donation_id: int
    sent_date: Optional[date] = None
    method: Optional[str] = None
    template_used: Optional[str] = None
    notes: Optional[str] = None


class ThankYouNoteCreate(ThankYouNoteBase):
    pass


class ThankYouNoteResponse(ThankYouNoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()