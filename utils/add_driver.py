def add_driver_to_db_url(db_url: str, driver: str = "psycopg2") -> str:
    if db_url.startswith("postgres://"):
        return db_url.replace("postgres://", "postgresql://", 1)
    return db_url