import os
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('PEDESIS_SETTINGS_MODULE', 'app.caisssa.settings')
if __name__ == '__main__':
    os.system("python manage.py run celery --debug")
