select
    rate_date,
    base_currency,
    target_currency,
    exchange_rate
from {{ source('raw', 'dim_exchange_rates') }}
where target_currency = 'USD'