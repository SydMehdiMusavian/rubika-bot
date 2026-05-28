from Rubika import Bot , MultiRunner , Text , ChatType , Reg , Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
import os , re , asyncio

TOKEN1 = "FIRST_BOT_TOKEN"
TOKEN2 = "SECOND_BOT_TOKEN"

bot1 = Bot(TOKEN1)
bot2 = Bot(TOKEN2)

@bot1.message(Text("ping"))
async def pong1(msg: Main_Update, fsm: StateInjection):
    await bot1.send_message_simple(ChatId=msg.chat_id, txt="pong from bot1")

@bot2.message(Text("ping"))
async def pong2(msg: Main_Update, fsm: StateInjection):
    await bot2.send_message_simple(ChatId=msg.chat_id, txt="pong from bot2")

if __name__ == "__main__":
    MultiRunner.Run(
        bot1(bot_name="FirstBot"),
        bot2(bot_name="SecondBot")
    )