import json

import requests

from usa import constants as consts
from usa.models import *


class CompanyCrawler:
    def crawl_companies(self):
        url = consts.URL_BODY_IEX + "/ref-data/symbols"
        url += "?token=" + consts.IEX_KEYS
        companies_json = json.loads(requests.get(url).text)

        companies = []
        for company_json in companies_json:
            company = Company()
            company.symbol = company_json["symbol"]
            company.iex_id = company_json["iexId"]
            company.name = company_json["name"]
            company.exchange = company_json["exchange"]
            company.save()
            companies.append(company)

        return companies
