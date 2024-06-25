import os
import json

from config import Config
from bot.logger import LOGGER
from .database.pg_impl import set_db


class BotSettings:
    def __init__(self):
        self.admins = Config.ADMINS

        db_users, _ = set_db.get_variable('AUTH_USERS')
        self.auth_users = json.loads(db_users) if db_users else []
        db_chats, _ = set_db.get_variable('AUTH_CHATS')
        self.auth_chats = json.loads(db_chats) if db_chats else []

        self.check_upload_mode()

        spam, _ = set_db.get_variable('ANTI_SPAM')
        self.anti_spam = spam if spam else 'OFF'

        public, _ = set_db.get_variable('BOT_PUBLIC')
        self.bot_public = True if public else False

        lang, _ = set_db.get_variable('BOT_LANGUAGE')
        self.bot_lang = lang if lang else 'en'

    def check_upload_mode(self):
        if os.path.exists('rclone.conf'):
            rclone = True
        elif Config.RCLONE_CONFIG:
            if Config.RCLONE_CONFIG.startswith('http'):
                rclone = requests.get(Config.RCLONE_CONFIG).content
                if response.status_code != 200:
                    LOGGER.info("RCLONE : Error retreiving file from Config URL")
                    self.rclone = False
                else:
                    with open('rclone.conf', 'w') as f:
                        f.write(rclone)
                    self.rclone=True
        else:
            self.rclone = False
            
        db_upload, _ = set_db.get_variable('UPLOAD_MODE')
        if self.rclone and db_upload == 'rclone':
            self.upload_mode = 'rclone'
        else:
            self.upload_mode = 'tg'

bot_set = BotSettings()