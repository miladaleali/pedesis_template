from pedesis.logger import logger

from pedesis.db.maker import init_all_tables
from pedesis.shortcuts import get_db

def main() -> None:
    logger.info("Creating initial data")
    init_all_tables()
    logger.info("Initial data created")

if __name__ == '__main__':
    main()
