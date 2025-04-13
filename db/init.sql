CREATE TABLE IF NOT EXISTS dim_comic (
    comic_id SERIAL PRIMARY KEY,
    comic_num INT NOT NULL,
    title VARCHAR(255),
    img_url VARCHAR(255),
    alt_text TEXT,
    year INT,
    month INT,
    day INT,
    safe_title VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fact_comic_views (
    fact_id SERIAL PRIMARY KEY,
    comic_id INT,
    views INT,
    cost DECIMAL(10, 2),
    review DECIMAL(3, 1),
    FOREIGN KEY (comic_id) REFERENCES dim_comic(comic_id)
);