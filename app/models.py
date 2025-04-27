from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session



# Replace with your actual Supabase PostgreSQL connection URL
host = 'aws-0-ap-southeast-1.pooler.supabase.com'
port = 6543
database_name = 'postgres'
username = 'postgres.afvsvhlwesqsdwmgrfgq'
password = 'upwork_automation_pass12'


DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

# DATABASE_URL = 'sqlite:///upwork_jobs_sql_25_08_2024__03_20_pkt.db'

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(String, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    createdDateTime = Column(DateTime)
    publishedDateTime = Column(DateTime)
    renewedDateTime = Column(DateTime, nullable=True)
    duration = Column(String)
    durationLabel = Column(String)
    engagement = Column(String)
    recordNumber = Column(String)
    experienceLevel = Column(String)
    freelancersToHire = Column(Integer)
    enterprise = Column(Text)
    totalApplicants = Column(Integer)
    preferredFreelancerLocation = Column(Text, nullable=True)  # Changed to Text
    preferredFreelancerLocationMandatory = Column(Text)
    premium = Column(Text)
    client_country = Column(String)
    client_total_hires = Column(Integer, nullable=True)
    client_total_posted_jobs = Column(Integer, nullable=True)
    client_total_spent = Column(Float, nullable=True)
    client_verification_status = Column(String, nullable=True)
    client_location_city = Column(String, nullable=True)
    client_location_state = Column(String, nullable=True)
    client_location_timezone = Column(String, nullable=True)
    client_location_offsetToUTC = Column(String, nullable=True)
    client_total_reviews = Column(Integer, nullable=True)
    client_total_feedback = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    team_name = Column(String, nullable=True)
    team_rid = Column(String, nullable=True)
    team_id = Column(String, nullable=True)
    team_photoUrl = Column(String, nullable=True)
    status = Column(String)
    category_id = Column(String)
    category_label = Column(String)
    subcategory_id = Column(String)
    subcategory_label = Column(String)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    threeLetterAbbreviation = Column(String, nullable=True)
    phoneCode = Column(String, nullable=True)
    avg_rate_bid = Column(Float, nullable=True)
    min_rate_bid = Column(Float, nullable=True)
    max_rate_bid = Column(Float, nullable=True)
    last_client_activity = Column(DateTime, nullable=True)
    invites_sent = Column(Integer, nullable=True)
    total_invited_to_interview = Column(Integer, nullable=True)
    total_hired = Column(Integer, nullable=True)
    total_unanswered_invites = Column(Integer, nullable=True)
    total_offered = Column(Integer, nullable=True)
    total_recommended = Column(Integer, nullable=True)
    skills = Column(Text, nullable=True)  # Changed to Text
    ciphertext = Column(String)
    JobUpdatedDateTime = Column(DateTime)
    
    JobFirstFetchedDateTime = Column(DateTime, default=func.now())