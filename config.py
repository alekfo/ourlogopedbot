from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
admin_id = int(os.getenv('ADMIN_ID'))
db_path = os.getenv('DATABASE_PATH')
