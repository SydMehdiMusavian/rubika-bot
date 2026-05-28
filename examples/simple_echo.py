from Rubika import Bot , MultiRunner , Text , ChatType , Reg , Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update
import os , re , asyncio

token = "Your Token"

app = Bot(Token=token)

@app.message(Text("hello", "سلام")) # هم برای hello اجرا میشه و هم برای سلام.
async def echo(msg: Main_Update, fsm: StateInjection):
    await app.send_message_simple(
        ChatId=msg.chat_id,
        txt=f"You said: {msg.message.text}"
    )

if __name__ == "__main__":
    app(bot_name="EchoBot").Run()