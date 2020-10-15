# 주식 거래 프로그램



* MSA 기반
  * stock-front-webapp
  * stock-capi-webapp(크롤러-crawler)
  * stock-aapi-webapp(분석-analyzer)
  * stock-tapi-webapp(매매-trader)
* Framework
  * 메인: Django
  * API: Flask



### 데이터베이스

- PER
  - COMPANY_CD / PER / DATE
- COMPANY
  - COMPANY_CD / COMPANY_NM / STARRED
- PRICE
  - COMPANY_CD / HIGHEST / LOWEST / OPENING / CLOSING / DATE