# in this file, do everything that must be done before python -m manage start station
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from pedesis.logger import logger
from pedesis.shortcuts import get_db, get_settings

max_tries = 60 * 5  # 5 minutes

wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logger.level('INFO').no),
    after=after_log(logger, logger.level('WARNING').no),
)
def init() -> None:
    try:
        db = get_db(get_settings().get_default_db_setting(), init_tables=False)
        with db.session() as s:
            s.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e

def main() -> None:
    logger.info("Initializing pedesis service")
    init()
    logger.info("Service finished initializing")


if __name__ == '__main__':
    main()
