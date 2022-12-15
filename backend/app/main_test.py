import os
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('PEDESIS_SETTINGS_MODULE', 'app.caisssa.settings')
# if __name__ == '__main__':
#     from pedesis.station.controller import Station
#     station = Station()
#     station.start()

from app.scalp import router