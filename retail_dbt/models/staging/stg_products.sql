select
    product_id,
    product_title,
    product_category,
    description,
    price,
    rating_rate,
    rating_count
from {{ source('raw', 'dim_products') }}