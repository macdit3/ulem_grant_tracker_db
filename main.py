# main.py
import os
from datetime import date, datetime
from typing import List, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, Float, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Load environment variables
load_dotenv()

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


# Initialize FastAPI app
app = FastAPI(title="ULEM Tracker API", description="API for ULEM donation tracking system")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API Endpoints

# Landing page or home route

@app.get("/")
def landing_page():
    return {"message": "Welcome to the ULM tracker API. Please contact Mac. at mac@ulem.org for any questions or issues.", "status": 200}



# Donors
@app.post("/donors/", response_model=DonorResponse, tags=["Donors"])
def create_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    db_donor = Donor(**donor.dict())
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor


@app.get("/donors/", response_model=List[DonorResponse], tags=["Donors"])
def read_donors(
        skip: int = 0,
        limit: int = 100,
        donor_type: Optional[str] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Donor)

    if donor_type:
        query = query.filter(Donor.donor_type == donor_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Donor.first_name.ilike(search_term)) |
            (Donor.last_name.ilike(search_term)) |
            (Donor.organization_name.ilike(search_term)) |
            (Donor.email.ilike(search_term))
        )

    return query.offset(skip).limit(limit).all()


@app.get("/donors/{donor_id}", response_model=DonorResponse, tags=["Donors"])
def read_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor


@app.put("/donors/{donor_id}", response_model=DonorResponse, tags=["Donors"])
def update_donor(donor_id: int, donor: DonorCreate, db: Session = Depends(get_db)):
    db_donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if db_donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")

    for key, value in donor.dict().items():
        setattr(db_donor, key, value)

    db_donor.updated_at = datetime.now()
    db.commit()
    db.refresh(db_donor)
    return db_donor


@app.delete("/donors/{donor_id}", response_model=DonorResponse, tags=["Donors"])
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")

    db.delete(donor)
    db.commit()
    return donor


# Programs
@app.post("/programs/", response_model=ProgramResponse, tags=["Programs"])
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@app.get("/programs/", response_model=List[ProgramResponse], tags=["Programs"])
def read_programs(
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        active_only: bool = False,
        db: Session = Depends(get_db)
):
    query = db.query(Program)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Program.name.ilike(search_term)) |
            (Program.description.ilike(search_term))
        )

    if active_only:
        today = date.today()
        query = query.filter(
            (Program.start_date <= today) &
            ((Program.end_date >= today) | (Program.end_date.is_(None)))
        )

    return query.offset(skip).limit(limit).all()


@app.get("/programs/{program_id}", response_model=ProgramResponse, tags=["Programs"])
def read_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@app.put("/programs/{program_id}", response_model=ProgramResponse, tags=["Programs"])
def update_program(program_id: int, program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = db.query(Program).filter(Program.id == program_id).first()
    if db_program is None:
        raise HTTPException(status_code=404, detail="Program not found")

    for key, value in program.dict().items():
        setattr(db_program, key, value)

    db_program.updated_at = datetime.now()
    db.commit()
    db.refresh(db_program)
    return db_program


@app.delete("/programs/{program_id}", response_model=ProgramResponse, tags=["Programs"])
def delete_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")

    db.delete(program)
    db.commit()
    return program


# Donations
@app.post("/donations/", response_model=DonationResponse, tags=["Donations"])
def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == donation.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if program exists (if program_id is provided)
    if donation.program_id:
        program = db.query(Program).filter(Program.id == donation.program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

    db_donation = Donation(**donation.dict())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)

    # Update program's current_progress if program_id is provided
    if donation.program_id:
        program = db.query(Program).filter(Program.id == donation.program_id).first()
        if program.current_progress is None:
            program.current_progress = 0
        program.current_progress += donation.amount
        program.updated_at = datetime.now()
        db.commit()

    return db_donation


@app.get("/donations/", response_model=List[DonationResponse], tags=["Donations"])
def read_donations(
        skip: int = 0,
        limit: int = 100,
        donor_id: Optional[int] = None,
        program_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Donation)

    if donor_id:
        query = query.filter(Donation.donor_id == donor_id)

    if program_id:
        query = query.filter(Donation.program_id == program_id)

    if start_date:
        query = query.filter(Donation.donation_date >= start_date)

    if end_date:
        query = query.filter(Donation.donation_date <= end_date)

    return query.offset(skip).limit(limit).all()


@app.get("/donations/{donation_id}", response_model=DonationResponse, tags=["Donations"])
def read_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@app.put("/donations/{donation_id}", response_model=DonationResponse, tags=["Donations"])
def update_donation(donation_id: int, donation: DonationCreate, db: Session = Depends(get_db)):
    db_donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if db_donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")

    # If program is being changed or amount is being updated, update program progress
    old_program_id = db_donation.program_id
    old_amount = db_donation.amount

    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == donation.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if program exists (if program_id is provided)
    if donation.program_id:
        program = db.query(Program).filter(Program.id == donation.program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

    for key, value in donation.dict().items():
        setattr(db_donation, key, value)

    db_donation.updated_at = datetime.now()
    db.commit()
    db.refresh(db_donation)

    # Update the progress for old program (if applicable)
    if old_program_id:
        old_program = db.query(Program).filter(Program.id == old_program_id).first()
        if old_program and old_program.current_progress is not None:
            old_program.current_progress -= old_amount
            old_program.updated_at = datetime.now()
            db.commit()

    # Update the progress for new program (if applicable)
    if db_donation.program_id:
        new_program = db.query(Program).filter(Program.id == db_donation.program_id).first()
        if new_program:
            if new_program.current_progress is None:
                new_program.current_progress = 0
            new_program.current_progress += db_donation.amount
            new_program.updated_at = datetime.now()
            db.commit()

    return db_donation


@app.delete("/donations/{donation_id}", response_model=DonationResponse, tags=["Donations"])
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")

    # Update program progress if applicable
    if donation.program_id:
        program = db.query(Program).filter(Program.id == donation.program_id).first()
        if program and program.current_progress is not None:
            program.current_progress -= donation.amount
            program.updated_at = datetime.now()
            db.commit()

    db.delete(donation)
    db.commit()
    return donation


# Pledges
@app.post("/pledges/", response_model=PledgeResponse, tags=["Pledges"])
def create_pledge(pledge: PledgeCreate, db: Session = Depends(get_db)):
    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == pledge.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if program exists (if program_id is provided)
    if pledge.program_id:
        program = db.query(Program).filter(Program.id == pledge.program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

    db_pledge = Pledge(**pledge.dict())
    db.add(db_pledge)
    db.commit()
    db.refresh(db_pledge)
    return db_pledge


@app.get("/pledges/", response_model=List[PledgeResponse], tags=["Pledges"])
def read_pledges(
        skip: int = 0,
        limit: int = 100,
        donor_id: Optional[int] = None,
        program_id: Optional[int] = None,
        status: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Pledge)

    if donor_id:
        query = query.filter(Pledge.donor_id == donor_id)

    if program_id:
        query = query.filter(Pledge.program_id == program_id)

    if status:
        query = query.filter(Pledge.status == status)

    return query.offset(skip).limit(limit).all()


@app.get("/pledges/{pledge_id}", response_model=PledgeResponse, tags=["Pledges"])
def read_pledge(pledge_id: int, db: Session = Depends(get_db)):
    pledge = db.query(Pledge).filter(Pledge.id == pledge_id).first()
    if pledge is None:
        raise HTTPException(status_code=404, detail="Pledge not found")
    return pledge


@app.put("/pledges/{pledge_id}", response_model=PledgeResponse, tags=["Pledges"])
def update_pledge(pledge_id: int, pledge: PledgeCreate, db: Session = Depends(get_db)):
    db_pledge = db.query(Pledge).filter(Pledge.id == pledge_id).first()
    if db_pledge is None:
        raise HTTPException(status_code=404, detail="Pledge not found")

    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == pledge.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if program exists (if program_id is provided)
    if pledge.program_id:
        program = db.query(Program).filter(Program.id == pledge.program_id).first()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

    for key, value in pledge.dict().items():
        setattr(db_pledge, key, value)

    db_pledge.updated_at = datetime.now()
    db.commit()
    db.refresh(db_pledge)
    return db_pledge


@app.delete("/pledges/{pledge_id}", response_model=PledgeResponse, tags=["Pledges"])
def delete_pledge(pledge_id: int, db: Session = Depends(get_db)):
    pledge = db.query(Pledge).filter(Pledge.id == pledge_id).first()
    if pledge is None:
        raise HTTPException(status_code=404, detail="Pledge not found")

    db.delete(pledge)
    db.commit()
    return pledge


# Tax Receipts
@app.post("/tax-receipts/", response_model=TaxReceiptResponse, tags=["Tax Receipts"])
def create_tax_receipt(tax_receipt: TaxReceiptCreate, db: Session = Depends(get_db)):
    # Check if donation exists
    donation = db.query(Donation).filter(Donation.id == tax_receipt.donor_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    db_tax_receipt = TaxReceipt(**tax_receipt.dict())
    db.add(db_tax_receipt)
    db.commit()
    db.refresh(db_tax_receipt)
    return db_tax_receipt


@app.get("/tax-receipts/", response_model=List[TaxReceiptResponse], tags=["Tax Receipts"])
def read_tax_receipts(
        skip: int = 0,
        limit: int = 100,
        donation_id: Optional[int] = None,
        generated_after: Optional[date] = None,
        generated_before: Optional[date] = None,
        sent: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    query = db.query(TaxReceipt)

    if donation_id:
        query = query.filter(TaxReceipt.donor_id == donation_id)  # donor_id is actually donation_id

    if generated_after:
        query = query.filter(TaxReceipt.generated_date >= generated_after)

    if generated_before:
        query = query.filter(TaxReceipt.generated_date <= generated_before)

    if sent is not None:
        if sent:
            query = query.filter(TaxReceipt.sent_date.isnot(None))
        else:
            query = query.filter(TaxReceipt.sent_date.is_(None))

    return query.offset(skip).limit(limit).all()


@app.get("/tax-receipts/{tax_receipt_id}", response_model=TaxReceiptResponse, tags=["Tax Receipts"])
def read_tax_receipt(tax_receipt_id: int, db: Session = Depends(get_db)):
    tax_receipt = db.query(TaxReceipt).filter(TaxReceipt.id == tax_receipt_id).first()
    if tax_receipt is None:
        raise HTTPException(status_code=404, detail="Tax receipt not found")
    return tax_receipt


@app.put("/tax-receipts/{tax_receipt_id}", response_model=TaxReceiptResponse, tags=["Tax Receipts"])
def update_tax_receipt(tax_receipt_id: int, tax_receipt: TaxReceiptCreate, db: Session = Depends(get_db)):
    db_tax_receipt = db.query(TaxReceipt).filter(TaxReceipt.id == tax_receipt_id).first()
    if db_tax_receipt is None:
        raise HTTPException(status_code=404, detail="Tax receipt not found")

    # Check if donation exists
    donation = db.query(Donation).filter(Donation.id == tax_receipt.donor_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    for key, value in tax_receipt.dict().items():
        setattr(db_tax_receipt, key, value)

    db_tax_receipt.updated_at = datetime.now()
    db.commit()
    db.refresh(db_tax_receipt)
    return db_tax_receipt


@app.delete("/tax-receipts/{tax_receipt_id}", response_model=TaxReceiptResponse, tags=["Tax Receipts"])
def delete_tax_receipt(tax_receipt_id: int, db: Session = Depends(get_db)):
    tax_receipt = db.query(TaxReceipt).filter(TaxReceipt.id == tax_receipt_id).first()
    if tax_receipt is None:
        raise HTTPException(status_code=404, detail="Tax receipt not found")

    db.delete(tax_receipt)
    db.commit()
    return tax_receipt


# Thank You Notes
@app.post("/thank-you-notes/", response_model=ThankYouNoteResponse, tags=["Thank You Notes"])
def create_thank_you_note(thank_you_note: ThankYouNoteCreate, db: Session = Depends(get_db)):
    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == thank_you_note.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if donation exists
    donation = db.query(Donation).filter(Donation.id == thank_you_note.donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    db_thank_you_note = ThankYouNote(**thank_you_note.dict())
    db.add(db_thank_you_note)
    db.commit()
    db.refresh(db_thank_you_note)
    return db_thank_you_note

@app.get("/thank-you-notes/", response_model=List[ThankYouNoteResponse], tags=["Thank You Notes"])
def read_thank_you_notes(
        skip: int = 0,
        limit: int = 100,
        donor_id: Optional[int] = None,
        donation_id: Optional[int] = None,
        sent: Optional[bool] = None,
        method: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(ThankYouNote)

    if donor_id:
        query = query.filter(ThankYouNote.donor_id == donor_id)

    if donation_id:
        query = query.filter(ThankYouNote.donation_id == donation_id)

    if sent is not None:
        if sent:
            query = query.filter(ThankYouNote.sent_date.isnot(None))
        else:
            query = query.filter(ThankYouNote.sent_date.is_(None))

    if method:
        query = query.filter(ThankYouNote.method == method)

    return query.offset(skip).limit(limit).all()


@app.get("/thank-you-notes/{thank_you_note_id}", response_model=ThankYouNoteResponse, tags=["Thank You Notes"])
def read_thank_you_note(thank_you_note_id: int, db: Session = Depends(get_db)):
    thank_you_note = db.query(ThankYouNote).filter(ThankYouNote.id == thank_you_note_id).first()
    if thank_you_note is None:
        raise HTTPException(status_code=404, detail="Thank you note not found")
    return thank_you_note


@app.put("/thank-you-notes/{thank_you_note_id}", response_model=ThankYouNoteResponse, tags=["Thank You Notes"])
def update_thank_you_note(thank_you_note_id: int, thank_you_note: ThankYouNoteCreate, db: Session = Depends(get_db)):
    db_thank_you_note = db.query(ThankYouNote).filter(ThankYouNote.id == thank_you_note_id).first()
    if db_thank_you_note is None:
        raise HTTPException(status_code=404, detail="Thank you note not found")

    # Check if donor exists
    donor = db.query(Donor).filter(Donor.id == thank_you_note.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Check if donation exists
    donation = db.query(Donation).filter(Donation.id == thank_you_note.donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    for key, value in thank_you_note.dict().items():
        setattr(db_thank_you_note, key, value)

    db_thank_you_note.updated_at = datetime.now()
    db.commit()
    db.refresh(db_thank_you_note)
    return db_thank_you_note


@app.delete("/thank-you-notes/{thank_you_note_id}", response_model=ThankYouNoteResponse, tags=["Thank You Notes"])
def delete_thank_you_note(thank_you_note_id: int, db: Session = Depends(get_db)):
    thank_you_note = db.query(ThankYouNote).filter(ThankYouNote.id == thank_you_note_id).first()
    if thank_you_note is None:
        raise HTTPException(status_code=404, detail="Thank you note not found")

    db.delete(thank_you_note)
    db.commit()
    return thank_you_note


# Additional utility endpoints

# Get donation summary by program
@app.get("/reports/donations-by-program/", tags=["Reports"])
def get_donations_by_program(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    result = []

    for program in programs:
        donations = db.query(Donation).filter(Donation.program_id == program.id).all()
        total_amount = sum(donation.amount for donation in donations)
        donor_count = len(set(donation.donor_id for donation in donations))

        result.append({
            "program_id": program.id,
            "program_name": program.name,
            "total_donations": len(donations),
            "total_amount": float(total_amount),
            "donor_count": donor_count,
            "goal_amount": float(program.goal_amount) if program.goal_amount else None,
            "progress_percentage": (float(total_amount) / float(program.goal_amount) * 100) if program.goal_amount else None
        })

    return result


# Get donation summary by donor
@app.get("/reports/donations-by-donor/", tags=["Reports"])
def get_donations_by_donor(db: Session = Depends(get_db)):
    donors = db.query(Donor).all()
    result = []

    for donor in donors:
        donations = db.query(Donation).filter(Donation.donor_id == donor.id).all()
        total_amount = sum(donation.amount for donation in donations)

        result.append({
            "donor_id": donor.id,
            "donor_name": f"{donor.first_name} {donor.last_name}" if donor.donor_type == "individual" else donor.organization_name,
            "donor_type": donor.donor_type,
            "total_donations": len(donations),
            "total_amount": float(total_amount),
            "first_donation_date": min([donation.donation_date for donation in donations]) if donations else None,
            "last_donation_date": max([donation.donation_date for donation in donations]) if donations else None
        })

    return result


# Get unfulfilled pledges
@app.get("/reports/unfulfilled-pledges/", tags=["Reports"])
def get_unfulfilled_pledges(db: Session = Depends(get_db)):
    unfulfilled_pledges = db.query(Pledge).filter(
        (Pledge.amount_fulfilled < Pledge.amount) |
        (Pledge.status != "fulfilled")
    ).all()

    result = []
    for pledge in unfulfilled_pledges:
        donor = db.query(Donor).filter(Donor.id == pledge.donor_id).first()
        program = db.query(Program).filter(Program.id == pledge.program_id).first() if pledge.program_id else None

        result.append({
            "pledge_id": pledge.id,
            "donor_id": pledge.donor_id,
            "donor_name": f"{donor.first_name} {donor.last_name}" if donor.donor_type == "individual" else donor.organization_name,
            "program_id": pledge.program_id,
            "program_name": program.name if program else None,
            "pledge_amount": float(pledge.amount),
            "amount_fulfilled": float(pledge.amount_fulfilled),
            "remaining_amount": float(pledge.amount - pledge.amount_fulfilled),
            "pledge_date": pledge.pledge_date,
            "status": pledge.status
        })

    return result


# Get pending thank you notes
@app.get("/reports/pending-thank-you-notes/", tags=["Reports"])
def get_pending_thank_you_notes(db: Session = Depends(get_db)):
    # Find donations without thank you notes
    donations = db.query(Donation).all()
    result = []

    for donation in donations:
        thank_you_note = db.query(ThankYouNote).filter(ThankYouNote.donation_id == donation.id).first()

        if not thank_you_note:
            donor = db.query(Donor).filter(Donor.id == donation.donor_id).first()

            result.append({
                "donation_id": donation.id,
                "donor_id": donor.id,
                "donor_name": f"{donor.first_name} {donor.last_name}" if donor.donor_type == "individual" else donor.organization_name,
                "donation_amount": float(donation.amount),
                "donation_date": donation.donation_date,
                "preferred_contact_method": donor.preferred_contact_method
            })

    return result


# Generate tax receipts for a specific year
@app.post("/tax-receipts/generate-for-year/", response_model=List[TaxReceiptResponse], tags=["Tax Receipts"])
def generate_tax_receipts_for_year(year: int, db: Session = Depends(get_db)):
    # Get all tax-deductible donations for the year without tax receipts
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    donations = db.query(Donation).filter(
        Donation.donation_date >= start_date,
        Donation.donation_date <= end_date,
        Donation.is_tax_deductible == True
    ).all()

    # Group donations by donor
    donor_donations = {}
    for donation in donations:
        # Check if a tax receipt already exists for this donation
        existing_receipt = db.query(TaxReceipt).filter(TaxReceipt.donor_id == donation.id).first()
        if existing_receipt:
            continue

        if donation.donor_id not in donor_donations:
            donor_donations[donation.donor_id] = []
        donor_donations[donation.donor_id].append(donation)

    # Create tax receipts
    generated_receipts = []
    for donor_id, donations in donor_donations.items():
        for donation in donations:
            tax_receipt = TaxReceipt(
                donor_id=donation.id,  # This field actually stores donation_id
                year_donated=start_date,  # First day of the year
                total_amount=donation.amount,
                generated_date=date.today(),
                sent_date=None
            )
            db.add(tax_receipt)
            db.commit()
            db.refresh(tax_receipt)
            generated_receipts.append(tax_receipt)

    return generated_receipts


# Create and setup the database tables
@app.on_event("startup")
async def startup():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)