import json

import requests

import usa.constants as consts
from usa.models import USACompany


class SymbolCrawler:
    def crawl_companies(self):
        url = consts.URL_BODY_IEX + "/ref-data/symbols"
        url += "?token=" + consts.IEX_KEYS
        print(url)
        companies_json = json.loads(requests.get(url).text)

        companies = []
        for company_json in companies_json:
            company = USACompany()
            company.symbol = company_json["symbol"]
            company.iex_id = company_json["iexId"]
            company.name = company_json["name"]
            company.exchange = company_json["exchange"]
            company.save()
            companies.append(companies)
        # USACompany.objects.all().bulk_create(companies)

        return companies
