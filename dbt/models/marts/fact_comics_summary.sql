SELECT
    f.fact_id,
    d.title_cleaned,
    f.views,
    f.cost,
    f.review
FROM {{ ref('stg_fact_comic_views') }} f
JOIN {{ ref('dim_comic_cleaned') }} d ON d.comic_id = f.comic_id
WHERE f.views > 100
