select
    o.order_id,
    o.customer_id,
    o.product_id,
    p.product_title,
    p.product_category,
    p.rating_rate,
    p.rating_count,
    o.quantity,
    o.local_price,
    o.currency,
    o.order_date,
    o.status,
    o.local_revenue,
    e.exchange_rate,
    (o.local_revenue * e.exchange_rate) as normalized_revenue_usd
from {{ ref('stg_internal_orders') }} o
left join {{ ref('stg_exchange_rates') }} e
    on o.order_date = e.rate_date
   and o.currency = e.base_currency
left join {{ ref('stg_products') }} p
    on o.product_id = p.product_id