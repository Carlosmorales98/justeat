import psycopg2

def validate_data(comic, views, review, cost):
    # Validate views
    if views < 0 or views > 10000:
        raise ValueError(f"The views should be between 0 and 10000, but it was obtained: {views}")
    
    # Validate cost
    if cost < 0:
        raise ValueError(f"The cost cannot be negative, but it was obtained: {cost}")
    
    # Validate reviews
    if review < 1.0 or review > 10.0:
        raise ValueError(f"The review should be between 1.0 and 10.0, but was obtained: {review}")

    # Validate mandatory fields of the comic
    if not comic.get('title') or not comic.get('img'):
        raise ValueError("Mandatory comic fields are missing: title or img_url")

def insert_to_db(comic, views, review, cost):
    try:
        validate_data(comic, views, review, cost)
        
        conn = psycopg2.connect(
            host="postgres",
            database="xkcd_db",
            user="airflow",
            password="airflow"
        )
        cur = conn.cursor()

        # Check if the comic already exists
        cur.execute("SELECT comic_id FROM dim_comic WHERE comic_num = %s", (comic['num'],))
        existing_comic = cur.fetchone()

        if existing_comic:
            print(f"The comic {comic['num']} already exists in the database.")
        else:
            # Insert comic in the dim_comic table
            cur.execute("""
                INSERT INTO dim_comic (comic_num, title, img_url, alt_text, year, month, day, safe_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING comic_id
            """, (
                comic['num'],
                comic['title'],
                comic['img'],
                comic['alt'],
                comic['year'],
                comic['month'],
                comic['day'],
                comic['safe_title']
            ))

            comic_id = cur.fetchone()[0]

            # Insert view and cost in fact_comic_views table
            cur.execute("""
                INSERT INTO fact_comic_views (comic_id, views, cost, review)
                VALUES (%s, %s, %s, %s)
            """, (comic_id, views, cost, review))

            conn.commit()

        cur.close()
        conn.close()
    except ValueError as e:
        print(f"Error inserting comic {comic['num']}: {e}")