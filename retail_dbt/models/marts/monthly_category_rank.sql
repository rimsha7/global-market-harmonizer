with product_category_sales as (
    select
        date_trunc('month', order_date) as month_sales,
        product_category,
        sum(normalized_revenue_usd) as total_category_revenue
    from {{ ref('fact_orders') }}
    group by month_sales, product_category
),

ranked_categories as (
    select
        month_sales,
        product_category,
        total_category_revenue,
        rank() over (
            partition by month_sales
            order by total_category_revenue desc
        ) as category_rank
    from product_category_sales
)

select
    month_sales,
    product_category,
    total_category_revenue,
    category_rank
from ranked_categories
where category_rank = 1
order by month_sales