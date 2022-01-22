from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
IP = env.str('ip')
DB_NAME = env.str('DB_NAME')
DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
DB_PORT = env.str('DB_PORT')
DB_PASS = env.str('DB_PASS')
QIWI = env.str('QIWI')
QIWI_NUMBER = env.str('QIWI_NUMBER')
QIWI_PUB = env.str('QIWI_PUB')
QIWI_SECRET = env.str('QIWI_SECRET')

POSTGRES_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

