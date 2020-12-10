select  t.symbol
      , t.date
      , (t.close
             / (    select  y.close
                    from    usa_daily_price y
                    where   1 = 1
                    and     y.symbol    = t.symbol
                    and       y.date      = t.date - 1)
        - 1)
        * 100 as rate
from    usa_daily_price t
where   1 = 1
and     symbol = 'AAPL'
;