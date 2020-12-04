### CONSTANT MANAGE ###


## URL
URL_BODY_NAVER = "https://finance.naver.com/"
URL_BODY_NAVER_REPORT = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd="

DART_KEY = "2e386fcc23f1246bdbf5b944c4299617db0a23a3"

DART_BS_LABELS = {"ifrsfullAssets": "total_assets", "ifrsfullLiabilities": "total_liabilities", "ifrsfullEquity": "total_equity"}
DART_IS_LABELS = {"ifrsfullProfitLoss": "net_income"}
DART_LABELS = {"bs": DART_BS_LABELS, "is": DART_IS_LABELS}

QUARTER_MAPPER = {"0331": "1", "0630": "2", "0930": "3", "1231": "4"}
ACCOUNT_MAPPER = {"자산총계": "total_assets", "자본총계": "total_equity", "당기순이익": "net_income"}
REPORT_CODE_MAPPER = {"4": "11011", "3": "11014", "2": "11012", "1": "11013"}
END_DATE_MAPPER = {"11011": "1231", "11014": "0930", "11012": "0630", "11013": "0331"}

## HEADER VALUE
HEADER_VALUE_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

INDICATORS = ["EPS", "PER", "BPS", "PBR", "업종PER"]
