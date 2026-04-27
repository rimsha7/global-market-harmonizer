select
    order_id,
    customer_id,
    product_id,
    quantity,
    local_price,
    currency,
    order_date,
    status,
    (quantity * local_price) as local_revenue
from {{ source('raw', 'internal_orders') }}