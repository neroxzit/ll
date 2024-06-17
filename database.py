import datetime
import motor.motor_asyncio
import config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.config = self.db.config

    def new_account(self, phone_number, full_name, username, user_id, session):
        return {
            "phone_number": phone_number,
            "full_name": full_name,
            "username": username,
            "user_id": user_id,
            "session": session,
            "join_date": datetime.date.today().isoformat()
        }

    async def add_account(self, account_data):
        await self.col.insert_one(account_data)

    async def is_account_exist(self, phone_number):
        account = await self.col.find_one({"phone_number": phone_number})
        return True if account else False

    async def total_accounts_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_accounts(self):
        all_accounts = self.col.find({})
        return all_accounts

    async def delete_account(self, phone_number):
        await self.col.delete_many({"phone_number": phone_number})

    async def find_account(self, phone_number):
        return await self.col.find_one({"phone_number": phone_number})

    async def set_session(self, phone_number, session):
        await self.col.update_one({"phone_number": phone_number}, {"$set": {"session": session}})

    async def get_session(self, phone_number):
        account = await self.col.find_one({"phone_number": phone_number})
        return account.get("session")

# مثال على كيفية الإعداد

db = Database(config.DB_URL, config.DB_NAME)
