
import os
import time
import json
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import requests
from flask import Flask, request, jsonify

# Define the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# Replace with your actual Supabase PostgreSQL connection URL
host = 'aws-0-us-east-2.pooler.supabase.com'
port = 6543
database_name = 'postgres'
username = 'postgres.wyrxhhpgnyvkpozcpbdz'
password = 'e2r7rYLqKbzm3LrW6kFOuB7R'


DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

# DATABASE_URL = 'sqlite:///upwork_jobs_sql_25_08_2024__03_20_pkt.db'

Base = declarative_base()

class JobToken(Base):
    __tablename__ = 'job_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String)

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
    contractor_selection = Column("contractor_selection", Text, nullable=True)


class JobFetcher:
    def __init__(self, database_url, client_id, client_secrect, refresh_token):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.api_token = self.get_token(client_id, client_secrect, refresh_token)
        print(f"Got Token: {self.api_token} for Refresh Token: {refresh_token}")
        
    def get_payload_query(self, include_spent_amount):
        
        if include_spent_amount:
            return """query GetMarketplaceJobPostings($searchType: MarketplaceJobPostingSearchType!, $marketPlaceJobFilter: MarketplaceJobPostingsSearchFilter!, $sortAttributes: [MarketplaceJobPostingSearchSortAttribute]) {
                marketplaceJobPostingsSearch(searchType: $searchType, marketPlaceJobFilter: $marketPlaceJobFilter , sortAttributes: $sortAttributes) {
                    totalCount
                    edges {
                        cursor
                        node {
                            id
                            job {
                                id
                                clientCompanyPublic {
                                    id
                                    legacyType
                                    teamsEnabled
                                    country {
                                        id
                                        name
                                        threeLetterAbbreviation
                                        region
                                        phoneCode
                                        relatedRegion {id name}
                                        relatedSubRegion {id name}
                                        active
                                    }
                                    state
                                    city
                                    timezone
                                    accountingEntity
                                }
                                classification {
                                    category {id ontologyId preferredLabel definition}
                                    subCategory {id ontologyId preferredLabel definition}
                                }
                                workFlowState {closeResult status}
                                annotations {tags}
                                activityStat {
                                    jobActivity {
                                        lastClientActivity
                                        invitesSent
                                        totalInvitedToInterview
                                        totalHired
                                        totalUnansweredInvites
                                        totalOffered
                                        totalRecommended
                                    }
                                    applicationsBidStats {
                                        avgRateBid {rawValue currency displayValue}
                                        minRateBid {rawValue currency displayValue}
                                        maxRateBid {rawValue currency displayValue}
                                        avgInterviewedRateBid {rawValue currency displayValue}
                                    }
                                }
                                contractorSelection {
                                    proposalRequirement {
                                        coverLetterRequired 
                                        freelancerMilestonesAllowed 
                                        screeningQuestions {
                                            question
                                        }
                                    } 
                                }
                                ownership {
                                    team {
                                        id
                                        rid
                                        name
                                        type
                                        legacyType
                                        flag {client vendor agency individual}
                                        hidden
                                        active
                                        photoUrl
                                        creationDate
                                        parentOrganization {id name}
                                    }
                                }
                            }
                            title
                            description
                            ciphertext
                            duration
                            durationLabel
                            engagement
                            amount {rawValue currency displayValue}
                            recordNumber
                            experienceLevel
                            freelancersToHire
                            enterprise
                            relevanceEncoded
                            totalApplicants
                            preferredFreelancerLocation
                            preferredFreelancerLocationMandatory
                            premium
                            clientNotSureFields
                            clientPrivateFields
                            applied
                            createdDateTime
                            publishedDateTime
                            renewedDateTime
                            client {
                                totalSpent {rawValue currency displayValue} 
                                memberSinceDateTime
                                totalHires
                                totalPostedJobs
                                verificationStatus
                                location {city state country timezone offsetToUTC}
                                totalReviews
                                totalFeedback
                                companyRid
                                companyName
                                edcUserId
                                lastContractPlatform
                                lastContractRid
                                lastContractTitle
                                hasFinancialPrivacy
                            }
                            skills {name prettyName highlighted}
                            hourlyBudgetType
                            hourlyBudgetMin {rawValue currency displayValue}
                            hourlyBudgetMax {rawValue currency displayValue}
                            localJobUserDistance
                            weeklyBudget {rawValue currency displayValue}
                            engagementDuration {id weeks label}
                            totalFreelancersToHire
                            teamId
                            freelancerClientRelation {
                                companyRid
                                companyName
                                edcUserId
                                lastContractPlatform
                                lastContractRid
                                lastContractTitle
                            }
                        }
                    }
                    pageInfo {endCursor hasNextPage}
                }
            }"""
        
        return """query GetMarketplaceJobPostings($searchType: MarketplaceJobPostingSearchType!, $marketPlaceJobFilter: MarketplaceJobPostingsSearchFilter!, $sortAttributes: [MarketplaceJobPostingSearchSortAttribute]) {
                marketplaceJobPostingsSearch(searchType: $searchType, marketPlaceJobFilter: $marketPlaceJobFilter , sortAttributes: $sortAttributes) {
                    totalCount
                    edges {
                        cursor
                        node {
                            id
                            job {
                                id
                                clientCompanyPublic {
                                    id
                                    legacyType
                                    teamsEnabled
                                    country {
                                        id
                                        name
                                        threeLetterAbbreviation
                                        region
                                        phoneCode
                                        relatedRegion {id name}
                                        relatedSubRegion {id name}
                                        active
                                    }
                                    state
                                    city
                                    timezone
                                    accountingEntity
                                }
                                classification {
                                    category {id ontologyId preferredLabel definition}
                                    subCategory {id ontologyId preferredLabel definition}
                                }
                                workFlowState {closeResult status}
                                annotations {tags}
                                activityStat {
                                    jobActivity {
                                        lastClientActivity
                                        invitesSent
                                        totalInvitedToInterview
                                        totalHired
                                        totalUnansweredInvites
                                        totalOffered
                                        totalRecommended
                                    }
                                    applicationsBidStats {
                                        avgRateBid {rawValue currency displayValue}
                                        minRateBid {rawValue currency displayValue}
                                        maxRateBid {rawValue currency displayValue}
                                        avgInterviewedRateBid {rawValue currency displayValue}
                                    }
                                }
                                contractorSelection {
                                    proposalRequirement {
                                        coverLetterRequired 
                                        freelancerMilestonesAllowed 
                                        screeningQuestions {
                                            question
                                        }
                                    } 
                                }
                                ownership {
                                    team {
                                        id
                                        rid
                                        name
                                        type
                                        legacyType
                                        flag {client vendor agency individual}
                                        hidden
                                        active
                                        photoUrl
                                        creationDate
                                        parentOrganization {id name}
                                    }
                                }
                            }
                            title
                            description
                            ciphertext
                            duration
                            durationLabel
                            engagement
                            amount {rawValue currency displayValue}
                            recordNumber
                            experienceLevel
                            freelancersToHire
                            enterprise
                            relevanceEncoded
                            totalApplicants
                            preferredFreelancerLocation
                            preferredFreelancerLocationMandatory
                            premium
                            clientNotSureFields
                            clientPrivateFields
                            applied
                            createdDateTime
                            publishedDateTime
                            renewedDateTime
                            client {
                                memberSinceDateTime
                                totalHires
                                totalPostedJobs
                                verificationStatus
                                location {city state country timezone offsetToUTC}
                                totalReviews
                                totalFeedback
                                companyRid
                                companyName
                                edcUserId
                                lastContractPlatform
                                lastContractRid
                                lastContractTitle
                                hasFinancialPrivacy
                            }
                            skills {name prettyName highlighted}
                            hourlyBudgetType
                            hourlyBudgetMin {rawValue currency displayValue}
                            hourlyBudgetMax {rawValue currency displayValue}
                            localJobUserDistance
                            weeklyBudget {rawValue currency displayValue}
                            engagementDuration {id weeks label}
                            totalFreelancersToHire
                            teamId
                            freelancerClientRelation {
                                companyRid
                                companyName
                                edcUserId
                                lastContractPlatform
                                lastContractRid
                                lastContractTitle
                            }
                        }
                    }
                    pageInfo {endCursor hasNextPage}
                }
            }"""

    def fetch_jobs(self,include_spent_amount,  category_ids, sub_category_id, offset=0, limit=10):
        url = "https://api.upwork.com/graphql"

        marketplaceJobFilter = {
                    "categoryIds_any": category_ids,
                    "clientHiresRange_eq": {"rangeStart": 0, "rangeEnd": 1} if not include_spent_amount else {"rangeStart": 1, "rangeEnd": 1000},
                    "pagination_eq": {"after": str(offset), "first": limit}
                }

        if sub_category_id != -1:
            marketplaceJobFilter["subcategoryIds_any"] = [sub_category_id,]

    #                                     totalSpent {rawValue currency displayValue}

        print(marketplaceJobFilter)
        payload = json.dumps({
            "query": self.get_payload_query(include_spent_amount),
            "variables": {
                "marketPlaceJobFilter": marketplaceJobFilter,
                "searchType": "USER_JOBS_SEARCH",
                "sortAttributes": [{"field": "RECENCY"}]
            }
        })

        headers = {
            'Authorization': f"bearer {self.api_token}",
            'Content-Type': 'application/json',
        }

        try:
    #         print(payload)
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Fetching json {data}")
    #         print(data)
            job_postings = data['data']['marketplaceJobPostingsSearch']['edges']
            page_info = data['data']['marketplaceJobPostingsSearch']['pageInfo']

            totalCount = data['data']['marketplaceJobPostingsSearch']['totalCount']
            logging.info(f"Fetched {len(job_postings)} jobs for category {category_ids} with offset {offset} and totalCount {totalCount}")

            return job_postings, page_info

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
        except KeyError as e:
            logging.error(f"Key error in the response data: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {e}")

        return None, None

    def insert_jobs(self, records):
        session = self.Session()
        try:
            for record in records:
                logging.debug(f"inserting job: {record}")
                job = Job(
                    id=record['id'],
                    title=record['title'],
                    description=record['description'],
                    createdDateTime=record['createdDateTime'],
                    publishedDateTime=record['publishedDateTime'],
                    renewedDateTime=record['renewedDateTime'],
                    duration=record['duration'],
                    durationLabel=record['durationLabel'],
                    engagement=record['engagement'],
                    recordNumber=record['recordNumber'],
                    experienceLevel=record['experienceLevel'],
                    freelancersToHire=record['freelancersToHire'],
                    enterprise=record['enterprise'],
                    totalApplicants=record['totalApplicants'],
                    preferredFreelancerLocation=json.dumps(record['preferredFreelancerLocation']),
                    preferredFreelancerLocationMandatory=record['preferredFreelancerLocationMandatory'],
                    premium=record['premium'],
                    client_country=record['client_country'],
                    client_total_hires=record['client_total_hires'],
                    client_total_posted_jobs=record['client_total_posted_jobs'],
                    client_total_spent=record['client_total_spent'],
                    client_verification_status=record['client_verification_status'],
                    client_location_city=record['client_location_city'],
                    client_location_state=record['client_location_state'],
                    client_location_timezone=record['client_location_timezone'],
                    client_location_offsetToUTC=record['client_location_offsetToUTC'],
                    client_total_reviews=record['client_total_reviews'],
                    client_total_feedback=record['client_total_feedback'],
                    amount=record['amount'],
                    currency=record['currency'],
                    team_name=record['team_name'],
                    team_rid=record['team_rid'],
                    team_id=record['team_id'],
                    team_photoUrl=record['team_photoUrl'],
                    status=record['status'],
                    category_id=record['category_id'],
                    category_label=record['category_label'],
                    subcategory_id=record['subcategory_id'],
                    subcategory_label=record['subcategory_label'],
                    city=record['city'],
                    state=record['state'],
                    country=record['country'],
                    threeLetterAbbreviation=record['threeLetterAbbreviation'],
                    phoneCode=record['phoneCode'],
                    avg_rate_bid=record['avg_rate_bid'],
                    min_rate_bid=record['min_rate_bid'],
                    max_rate_bid=record['max_rate_bid'],
                    last_client_activity=record['last_client_activity'],
                    invites_sent=record['invites_sent'],
                    total_invited_to_interview=record['total_invited_to_interview'],
                    total_hired=record['total_hired'],
                    total_unanswered_invites=record['total_unanswered_invites'],
                    total_offered=record['total_offered'],
                    total_recommended=record['total_recommended'],
                    skills=record['skills'],
                    ciphertext=record['ciphertext'],
                    JobUpdatedDateTime = datetime.now(timezone.utc),
                    contractor_selection=record['contractor_selection']
                )
                session.merge(job)  # Use merge to insert or update records
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error inserting jobs: {e}")
        finally:
            session.close()

    def fetch_and_store_jobs(self,include_spent_amount, category_ids, sub_category_id, timestamp_24_hours_ago, limit=10, max_records = 100):
        offset = 0
        while True:
            job_postings, page_info = self.fetch_jobs(include_spent_amount, category_ids, sub_category_id, offset, limit)
            if job_postings is None:
                break
    
            records = []
            for job in job_postings:
                if not job:
                    continue
                node = job['node']
                job_info = node['job']
                client_info = job_info['clientCompanyPublic']
                classification_info = job_info['classification']
                workflow_state = job_info['workFlowState']
                activity_stat = job_info['activityStat']
                applications_bid_stats = activity_stat['applicationsBidStats'] if activity_stat else {}
                job_activity = activity_stat['jobActivity'] if activity_stat else {}
                contractor_selection = json.dumps(job_info['contractorSelection'] if job_info['contractorSelection'] else {})
                ownership_team = job_info['ownership']['team'] if job_info['ownership'] and job_info['ownership']['team'] else {}
                client_location = node['client']['location'] if node['client'] else {}

                client_info_country =  client_info.get('country') if client_info.get('country') else {}

                job_record = {
                    'id': node['id'],
                    'title': node['title'],
                    'description': node['description'],
                    'createdDateTime': datetime.strptime(node['createdDateTime'], '%Y-%m-%dT%H:%M:%S%z'),
                    'publishedDateTime': datetime.strptime(node['publishedDateTime'], '%Y-%m-%dT%H:%M:%S%z'),
                    'renewedDateTime': datetime.strptime(node['renewedDateTime'], '%Y-%m-%dT%H:%M:%S%z') if node['renewedDateTime'] else None,
                    'duration': node['duration'],
                    'durationLabel': node['durationLabel'],
                    'engagement': node['engagement'],
                    'recordNumber': node['recordNumber'],
                    'experienceLevel': node['experienceLevel'],
                    'freelancersToHire': node['freelancersToHire'],
                    'enterprise': node['enterprise'],
                    'totalApplicants': node['totalApplicants'],
                    'preferredFreelancerLocation': node['preferredFreelancerLocation'],
                    'preferredFreelancerLocationMandatory':  '',
                    'premium': node['premium'],
                    'client_country': client_location.get('country', None),
                    'client_total_hires': node['client']['totalHires'] if node['client'] else 0,
                    'client_total_posted_jobs': node['client']['totalPostedJobs'] if node['client'] else 0,
                    'client_total_spent': node['client']['totalSpent']['rawValue'] if node.get('client') and node['client'].get('totalSpent') else 0,
                    'client_verification_status': node['client']['verificationStatus'] if node['client'] else None,
                    'client_location_city': client_location.get('city', None),
                    'client_location_state': client_location.get('state', None),
                    'client_location_timezone': client_location.get('timezone', None),
                    'client_location_offsetToUTC': client_location.get('offsetToUTC', None),
                    'client_total_reviews': node['client']['totalReviews'] if node['client'] else None,
                    'client_total_feedback': node['client']['totalFeedback'] if node['client'] else None,
                    'amount': node['amount']['rawValue'] if node['amount'] else None,
                    'currency': node['amount']['currency'] if node['amount'] else None,
                    'team_name': ownership_team.get('name', None),
                    'team_rid': ownership_team.get('rid', None),
                    'team_id': ownership_team.get('id', None),
                    'team_photoUrl': ownership_team.get('photoUrl', None),
                    'status': workflow_state.get('status', None),
                    'category_id': classification_info['category']['id'] if classification_info and classification_info['category'] else None,
                    'category_label': classification_info['category']['preferredLabel'] if classification_info and classification_info['category'] else None,
                    'subcategory_id': classification_info['subCategory']['id'] if classification_info and classification_info['subCategory'] else None,
                    'subcategory_label': classification_info['subCategory']['preferredLabel'] if classification_info and classification_info['subCategory'] else None,
                    'city': client_info.get('city', None),
                    'state': client_info.get('state', None),
                    'country': client_info_country.get('name', None),
                    'threeLetterAbbreviation': client_info_country.get('threeLetterAbbreviation', None),
                    'phoneCode': client_info_country.get('phoneCode', None),
                    'avg_rate_bid': applications_bid_stats['avgRateBid']['rawValue'] if applications_bid_stats and applications_bid_stats.get('avgRateBid') else None,
                    'min_rate_bid': applications_bid_stats['minRateBid']['rawValue'] if applications_bid_stats and applications_bid_stats.get('minRateBid') else None,
                    'max_rate_bid': applications_bid_stats['maxRateBid']['rawValue'] if applications_bid_stats and applications_bid_stats.get('maxRateBid') else None,
                    'last_client_activity': datetime.strptime(job_activity.get('lastClientActivity'), '%Y-%m-%dT%H:%M:%S.%fZ') if job_activity.get('lastClientActivity') else None,
                    'invites_sent': job_activity.get('invitesSent', None),
                    'total_invited_to_interview': job_activity.get('totalInvitedToInterview', None),
                    'total_hired': job_activity.get('totalHired', None),
                    'total_unanswered_invites': job_activity.get('totalUnansweredInvites', None),
                    'total_offered': job_activity.get('totalOffered', None),
                    'total_recommended': job_activity.get('totalRecommended', None),
                    'skills': ', '.join([skill['name'] for skill in node['skills']]) if node['skills'] else None,
                    'ciphertext': node['ciphertext'],
                    'contractor_selection': contractor_selection,
                }
                records.append(job_record)

            max_job_created_date_safe = max(job['createdDateTime'] for job in records if job)
            min_job_created_date_safe = min(job['createdDateTime'] for job in records if job)

            print(max_job_created_date_safe, min_job_created_date_safe)

            if max_job_created_date_safe < timestamp_24_hours_ago:
                logging.info(f"breaking off at offset {offset} due to date in past. max job date : {max_job_created_date_safe} . min job date : {min_job_created_date_safe} compared with: {timestamp_24_hours_ago}")
                break

            self.insert_jobs(records)

            if not page_info['hasNextPage']:
                break

            offset = int(page_info['endCursor'])

            if offset >= max_records:
                break

            time.sleep(2)

        logging.info(f"offset {offset}")
    
    def get_token(self, client_id, client_secret, refresh_token):
        
        with self.Session() as session:
            first_record = session.query(JobToken).first()
            if first_record and first_record.token:
                refresh_token = first_record.token
            
            url = "https://www.upwork.com/api/v3/oauth2/token"

            payload = f'grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())

            new_refresh_token = response.json()['refresh_token']
            
            if first_record:
                first_record.token = new_refresh_token
            else:
                # Insert a new record if none exists
                first_record = JobToken(token=new_refresh_token)
                session.add(first_record)
            
            session.commit()

        return response.json()['access_token']
        

    def call(self, include_spent_amount, category_id, sub_category_id, limit, max_records, minutes):
        
        # Get the current time in UTC
        current_time = datetime.now(timezone.utc)
        # Calculate the timestamp for 24 hours ago
        timestamp_10_minutes_ago = current_time - timedelta(minutes=minutes)
        
        self.fetch_and_store_jobs(include_spent_amount, category_id, sub_category_id, timestamp_10_minutes_ago, limit, max_records)



@app.route('/fetch-jobs', methods=['GET'])
def fetch_jobs():
    refresh_token = "oauth2v2_dc00cd5bd56b31a92fd05d242a786757"
    client_id = "30c1dc1fcd709c4423719e3eb838424b"
    client_secret = "425b9cdaefc27b19"
    
    
    
    job_fetcher = JobFetcher(DATABASE_URL, client_id, client_secret, refresh_token)

    # category_ids = {
    # '531770282580668420': [-1],
    # '531770282580668419': [-1],
    # '531770282580668418': [-1],
    # }
    
    category_ids = {
        '531770282584862721': [-1],
        '531770282580668416': [-1],
        '531770282580668417': [-1],
        '531770282580668420': [-1],
        '531770282580668421': [-1],
        '531770282584862722': [-1],
        '531770282580668419': [-1],
        '531770282584862723': [-1],
        '531770282580668422': [-1],
        '531770282584862720': [-1],
        '531770282580668418': [-1],
        '531770282580668423': [-1],
    }


    limit = 100
    max_records = 5000
    
    minutes = int(request.args.get('minutes', 30))
    logging.info(f"Fetching for last {minutes} minutes")
    
    for include_spent_amount in (False, True):
        job_fetcher.call(include_spent_amount, list(category_ids.keys()), -1, limit, max_records, minutes)
    
    time.sleep(10)
    logging.info("Data fetching and storing complete.")  
    
    return jsonify({"status": "success", "message": "Jobs fetched and stored successfully"}), 200

@app.route('/refresh-client-aggregates', methods=['POST'])
def refresh_client_aggregates():
    """
    Endpoint to refresh the client_aggregates materialized view.
    """
    try:
        engine = create_engine(DATABASE_URL)
        with engine.begin() as connection:
            # Refresh the materialized view
            connection.execute(text("REFRESH MATERIALIZED VIEW client_aggregates"))
        
        logging.info("Successfully refreshed client_aggregates view")
        return jsonify({
            "status": "success",
            "message": "client_aggregates view refreshed successfully"
        }), 200
    
    except Exception as e:
        logging.error(f"Error refreshing client_aggregates view: {e}")
        return jsonify({
            "status": "error",
            "message": f"Failed to refresh client_aggregates view: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))