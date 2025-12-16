def add_driver_to_db_url(db_url: str, driver: str = "psycopg2") -> str:
    if db_url.startswith("postgres://"):
        return db_url.replace("postgresql://", f"postgresql+{driver}://", 1)
    return db_url