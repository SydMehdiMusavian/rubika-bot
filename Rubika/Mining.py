import json, copy, asyncio
from Rubika.FinitState import StateInjection
from Rubika.FileLock import GlobalFileLock
class Fetch_Data:

    @staticmethod
    async def save_dict_to_json(user_dict, filename):
        cp_user_dict = {}
        if user_dict != {}:
            cp_user_dict = copy.deepcopy(user_dict)
            for i, j in cp_user_dict.items():
                cp_user_dict[i]["state"] = {
                    "name": j["state"].name,
                    "next": j["state"].next_name,
                    "previus": j["state"].previous_name
                }

        def _sync_save():
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(cp_user_dict, f, ensure_ascii=False, indent=4)

        async with GlobalFileLock.get_lock():
            await asyncio.to_thread(_sync_save)

    @classmethod
    async def monitor_and_save(cls, interval: int, f_name: str):
        while True:
            snapshot = copy.deepcopy(StateInjection.user_state)
            await cls.save_dict_to_json(user_dict=snapshot, filename=f_name)
            await asyncio.sleep(interval)