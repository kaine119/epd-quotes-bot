import logging
from telegram.ext import ApplicationBuilder

from commands import admin_delete_sticker, user_add_sticker, admin_create_pack

import yaml

with open("credentials.yml", "r") as f:
    credentials = yaml.safe_load(f)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = credentials['token']
ADMIN_USER_ID = credentials['admin_user_id']

admin_delete_sticker.set_admin_id(ADMIN_USER_ID)
admin_create_pack.set_admin_id(ADMIN_USER_ID)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()


    application.add_handler(user_add_sticker.handler)

    application.add_handler(admin_delete_sticker.handler)
    application.add_handler(admin_create_pack.handler)


    application.run_polling()
