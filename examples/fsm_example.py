from Rubika import Bot , MultiRunner , Text , ChatType , Reg , Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
import os , re , asyncio

TOKEN = "YOUR_BOT_TOKEN"
app = Bot(TOKEN)

class RegState(state_group):
    START = state()
    WAIT_NAME = state()
    WAIT_AGE = state()

@app.message(Text("in") & ChatType("User"))
async def register_state(msg: Main_Update, fsm: StateInjection):
    await fsm.set_state(RegState.START)
    await app.send_message_simple(ChatId=msg.chat_id , txt="Now send me start")

@app.message(Text("start") & StateFilter(RegState.START) & ChatType("User"))
async def start(msg: Main_Update, fsm: StateInjection):
    await fsm.set_state(RegState.WAIT_NAME)
    await app.send_message_simple(ChatId=msg.chat_id, txt="Enter your name:")

@app.message(StateFilter(RegState.WAIT_NAME) & ChatType("User"))
async def get_name(msg: Main_Update, fsm: StateInjection):
    name = msg.message.text
    await fsm.set_state(RegState.WAIT_AGE, data={"name": name})
    await app.send_message_simple(ChatId=msg.chat_id , txt=f"Hi {name}, now enter your age:")

@app.message(StateFilter(RegState.WAIT_AGE) & ChatType("User"))
async def finish(msg: Main_Update, fsm: StateInjection):
    age = msg.message.text
    data = await fsm.get_state_Data()
    await fsm.clear_state()
    await app.send_message_simple(ChatId=msg.chat_id, txt=f"Saved: {data['name']}, age {age}")

if __name__ == "__main__":
    app(bot_name="FSMBot").Run()