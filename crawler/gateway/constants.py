### CONSTANT MANAGE ###


## URL
URL_BODY_NAVER = "https://finance.naver.com/"
URL_BODY_NAVER_REPORT = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd="

DART_KEY = "2e386fcc23f1246bdbf5b944c4299617db0a23a3"

DART_BS_LABELS = {"ifrsfullAssets": "total_assets", "ifrsfullLiabilities": "total_liabilities", "ifrsfullEquity": "total_equity"}
DART_IS_LABELS = {"ifrsfullProfitLoss": "net_income"}
DART_LABELS = {"bs": DART_BS_LABELS, "is": DART_IS_LABELS}

QUARTER_MAPPER = {"0331": "1", "0630": "2", "0930": "3", "1231": "4"}

## HEADER VALUE
HEADER_VALUE_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

INDICATORS = ["EPS", "PER", "BPS", "PBR", "업종PER"]
