import logging
import time
import requests
from pydantic import BaseModel
from pathlib import Path
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, BigInteger
import json
from ...db.base import Base
from sqlalchemy import (
    Column,
    Float,
)
from sqlalchemy.types import JSON

logger = logging.getLogger(__name__)

class SB1Accounts(Base):
    __tablename__ = "sb1accounts"
    account_number = Column(BigInteger, primary_key=True)



class SB1Transactions(Base):
    __tablename__ = "sb1transactions"

    # Primary key
    id = Column(String, primary_key=True)

    # Dates
    date = Column(Date)
    value_date = Column(Date)
    booked_date = Column(Date, primary_key=True)
    posting_date = Column(Date)

    # Core transaction info
    _type = Column(String)
    amount = Column(Float)

    type_code = Column(String)
    type_text = Column(String)

    description = Column(String)
    cleaned_description = Column(String)
    original_description = Column(String)

    # Account info
    account_key = Column(String)
    account_name = Column(String)
    account_number = Column(BigInteger, primary_key=True)

    remote_account_name = Column(String)
    remote_account_number = Column(String)

    # Currency info
    currency_code = Column(String)
    currency_amount = Column(Float)
    account_currency = Column(String)
    exchange_rate = Column(Float)

    # References
    kid_or_message = Column(String)
    payment_reference = Column(String)
    archive_reference = Column(String, primary_key=True)
    numerical_reference = Column(String)
    non_unique_id = Column(String)

    # Misc
    e_invoice_url = Column(String)

    # 🔑 Nested structures stored as JSON
    payment_details = Column(JSON)
    classification_input = Column(JSON)


class SB1API:
    def __init__(self, user: str, cache_dir: Path, credentials_dir: Path, sleeptime: int = 60, authenticate = False):
        self._attempts = 0
        self.sleeptime = sleeptime
        self.user = user
        self.cache_dir = cache_dir
        self.credentials_dir = credentials_dir
        self.is_valid()

        if authenticate:
            self.authenticate()
        # self.test()

    def is_valid(self):
        if not isinstance(self.cache_dir, Path):
            raise TypeError()
        if not isinstance(self.credentials_dir, Path):
            raise TypeError()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.credentials_dir.mkdir(parents=True, exist_ok=True)
    
    def send_request(self, method, url, **kwargs):
        self._attempts+1
        if self._attempts > 5:
            raise RuntimeError(f"Something is wrong, request has failed {self._attempts} times!")
        try:
            r = requests.request(method=method, url=url, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            if r.status_code == 401:
                self.refresh_token()
                return self.send_request(method=method, url=url, **kwargs)
            else:
                logger.error(r.status_code)
                raise e
        except Exception as e:
            raise e
        finally:
            self._attempts=0
            time.sleep(self.sleeptime)
            

    def test(self):
        r = self.send_request(
            method="POST",
            url="https://api.sparebank1.no/common/helloworld",
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
        )
        

    def store_credentials(self):
        ...
    
    def get_credentials(self):
        credentials = json.load(open(f"{self.credentials_dir}/credentials.json"))
        return credentials["CLIENT_ID"], credentials["CLIENT_SECRET"]

    def authenticate(self):
        """Authenticate to the API and get a token using credentials."""
        logger.info("Starting authentication process")
        client_id, client_secret = self.get_credentials()
        token = self.send_request(
            method="POST",
            url="https://api-auth.sparebank1.no/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": input("Enter the code from the URL: "),
                "grant_type": "authorization_code",
                "state": input("Enter the state from the URL: "),
                "redirect_uri": input("Enter the redirect URI: "),
                "scope": "read_only",
            },
        ).json()
        self.write_token(token)
        logger.info("Authentication done, token written to file. Taking a little nap.")


    def write_token(self, token):
        with open(f"{self.credentials_dir}/token.json", "w") as outfile:
            outfile.write(json.dumps(token))

    def refresh_token(self):
        logger.info("Refreshing token")
        client_id, client_secret = self.get_credentials()
        refresh_token = json.load(open(f"{self.credentials_dir}/token.json"))["refresh_token"]
        new_token = self.send_request(
            method="POST",
            url="https://api-auth.sparebank1.no/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        ).json()
        if "error" in new_token.keys():
            logger.warning("Maybe authentication has expired.")
            raise Exception(
                "Something wrong with refresh:",
                new_token,
            )
        logger.info("Writing new token")
        self.write_token(new_token)

    def get_access_token(self):
        """Get the access token."""
        return json.load(open(f"{self.credentials_dir}/token.json"))["access_token"]


    def clear_cache_dir(self):
        logger.debug("Clearing cache")
        print("Test")
        for item in self.cache_dir.iterdir():
            if item.is_file():
                item.unlink()
        logger.debug("Clearing cache - completed")

    def get_user_list(self):
        ...
    
    def get_accounts(self):
        headers = {
            "accept": "application/vnd.sparebank1.v1+json; charset=utf-8",
            "Authorization": f"Bearer {self.get_access_token()}",
        }
        r = self.send_request(method="GET", url="https://api.sparebank1.no/personal/banking/accounts", headers=headers)
        with open(f"{self.cache_dir}/accounts.json", "w") as outfile:
            outfile.write(json.dumps(r.json(), indent=4, ensure_ascii=False))
        # Insert to database
        # self.clear_cache_dir()

    def get_transaction_list(self):
        'https://developer.sparebank1.no/transactions/export?accountKey=Qg3NwjAFQlHfKgwMDitQ&fromDate=2026-03-30&toDate=2026-04-05'

    def get_transaction_details(self):
        ...
    
    def collect_week(self, week, year):
        logger.info(f"Gathering transactions for {year}-{week}")
        try:
            self.get_transaction_list()
            # Get amount of transactions for month in database.
            # Compare number of transactions. Log info if same and skip week. If different log warning with totals and diff and try retrieve transactions for the week from scratch.
            self.get_transaction_details()
            # Verify number of transactions match.
            # Drop current in database for week.
            # Insert new into database. Log amount of duplicates
        except Exception as e:
            logger.error(f"Something went wrong! {e}", exc_info=True)
        finally:
            logger.debug("Clearing cache")
            self.clear_cache_dir()



if __name__ == "__main__":
    api_connector = SB1API(
        user = "Magnus",
        cache_dir= Path.home() / "Documents" / "data_cache", 
        credentials_dir= Path.home() / "Documents" / "datastore", 
        #authenticate=True
    )
    api_connector.get_accounts()
