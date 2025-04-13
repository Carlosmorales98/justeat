SELECT
    comic_id,
    comic_num,
    INITCAP(title) AS title_cleaned,
    year,
    month,
    day
FROM {{ ref('stg_dim_comic') }}
WHERE year > 2005
