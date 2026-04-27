create database if not exists retail_db;
create schema if not exists retail_db.raw;

create or replace table retail_db.raw.internal_orders(
  order_id number,
  customer_id number,
  product_id number,
  quantity number,
  local_price number(10,2),
  currency string,
  order_date date,
  status string
);

create or replace table retail_db.raw.dim_exchange_rates_json (
    data variant
);
create or replace table retail_db.raw.dim_products_json (
    data variant
);

create or replace file format retail_db.raw.orders_csv_format
type = csv
skip_header = 1
field_optionally_enclosed_by = '"'
null_if = ('NULL', 'null', '')
empty_field_as_null = true;

create or replace file format retail_db.raw.json_format
type = json;


create or replace storage integration s3_retail
type = external_stage
storage_provider = s3
enabled = true
storage_aws_role_arn = 'arn:aws:iam::516141620989:role/snowflake_s3_role_retail'
storage_allowed_locations = (
  's3://s3-retail-raw-zone/'
);

desc integration s3_retail;

create or replace stage retail_db.raw.retail_orders_stage
url = 's3://s3-retail-raw-zone/internal/'
storage_integration = s3_retail
file_format = retail_db.raw.orders_csv_format;

create or replace stage retail_db.raw.api_raw_stage
url = 's3://s3-retail-raw-zone/'
storage_integration = s3_retail
file_format = retail_db.raw.json_format;

list @retail_orders_stage;

copy into retail_db.raw.internal_orders
from @retail_db.raw.retail_orders_stage
files = ('orders.csv')
file_format = (format_name = retail_db.raw.orders_csv_format)
force = true
on_error = 'continue';

copy into retail_db.raw.dim_exchange_rates_json
from @retail_db.raw.api_raw_stage/2026/04/20/exchange_rates.json
file_format = (format_name = retail_db.raw.json_format)
force = true;

copy into retail_db.raw.dim_products_json
from @retail_db.raw.api_raw_stage/2026/04/20/products.json
file_format = (format_name = retail_db.raw.json_format)
force = true;

select count(*) from retail_db.raw.internal_orders;
select * from retail_db.raw.internal_orders limit 20;

create schema if not exists retail_db.analytics;

select * from retail_db.analytics.stg_internal_orders limit 10;

list @retail_db.raw.api_raw_stage/2026/04/20/;
list @retail_db.raw.retail_orders_stage;

select * from retail_db.raw.dim_exchange_rates_json limit 5;
select * from retail_db.raw.dim_products_json limit 5;

create or replace table retail_db.raw.dim_exchange_rates as
select
    e.value:date::date as rate_date,
    e.value:base_currency::string as base_currency,
    e.value:target_currency::string as target_currency,
    e.value:exchange_rate::float as exchange_rate
from retail_db.raw.dim_exchange_rates_json,
     lateral flatten(input => data) e;

create or replace table retail_db.raw.dim_products as
select
    p.value:product_id::number as product_id,
    p.value:product_title::string as product_title,
    p.value:product_category::string as product_category,
    p.value:description::string as description,
    p.value:price::float as price,
    coalesce(p.value:rating_rate::float, 0.0) as rating_rate,
    coalesce(p.value:rating_count::number, 0) as rating_count
from retail_db.raw.dim_products_json,
     lateral flatten(input => data) p;

select count(*) from retail_db.raw.dim_exchange_rates_json;
select count(*) from retail_db.raw.dim_products_json;

select data from retail_db.raw.dim_exchange_rates_json limit 5;
select data from retail_db.raw.dim_products_json limit 5;

select count(*) from retail_db.raw.dim_products;
select * from retail_db.raw.dim_products limit 10;

select data from retail_db.raw.dim_exchange_rates_json limit 1;
select * from retail_db.raw.dim_exchange_rates;