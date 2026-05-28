# Rubika Bot – Python Library for Rubika Bot API

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An **asynchronous** and **easy-to-use** Python framework for building bots on **Rubika** messenger.  
Inspired by `python-telegram-bot`, it provides a clean interface with filters, Finite State Machine (FSM), multi-bot support, file upload, inline keyboards, and more.

> **Note**: Rubika Bot API is currently limited to **long polling** (no webhook yet). This library handles polling efficiently.

---

## ✨ Features

- ✅ Full async support with `aiohttp`
- ✅ Simple decorator-based handlers (`@bot.message(...)`)
- ✅ Powerful filters: `Text`, `ChatType`, `RegEx`, `Documents`, `GeneralFilter` (poll, location, contact, delete)
- ✅ **Finite State Machine (FSM)** with `state_group`, auto‑saving to JSON file
- ✅ Run **multiple bots** simultaneously with `MultiRunner` (isolated logs via `contextvars`)
- ✅ Send & receive files (images, videos, audio, documents) – automatic upload flow
- ✅ Inline and floating keyboards, polls, location, contacts
- ✅ Ban/unban members, forward messages, edit messages
- ✅ Logging with file rotation and per‑bot identification

---

## 📦 Installation

```bash
pip install git+https://github.com/SydMehdiMusavian/rubika-bot.git
```
### Or clone and install manually:
```bash
git clone https://github.com/SydMehdiMusavian/rubika-bot.git
cd rubika-bot
pip install -r requirements.txt
python setup.py install
```

## 🚀 Quick Start

### Create a bot that echoes any text message:
```python
from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update

import os , re , asyncio

TOKEN = "your_bot_token_here"

app = Bot(TOKEN)

@app.message(Text("hello"))   # simple text filter
async def echo_handler(msg: Main_Update, fsm: StateInjection):
    await app.send_message_simple(
        ChatId=msg.chat_id,
        txt=f"You said: {msg.message.text}"
    )

if __name__ == "__main__":
    app(bot_name="EchoBot").Run()
```

## 🔧 Examples
- 1️⃣ Using Filters & Keyboards
```python
from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update

@app.message(Document_Object.picture & ChatType("User"))
async def handle_photo(msg: Main_Update, fsm: StateInjection):
    await app.send_message_simple(msg.chat_id, "Nice photo!")

@app.message(F.poll)
async def handle_poll(msg: Main_Update, fsm: StateInjection):
    await app.send_message_simple(msg.chat_id, "Thanks for the poll!")
```
- 2️⃣ Finite State Machine (FSM)
```python
from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update

class MyStates(state_group):
    START = state()
    WAITING_NAME = state()
    WAITING_AGE = state()

@app.message(Text("start") & StateFilter(MyStates.START))
async def start_cmd(msg: Main_Update, fsm: StateInjection):
    await fsm.set_state(MyStates.WAITING_NAME)
    await app.send_message_simple(msg.chat_id, "Enter your name:")

@app.message(StateFilter(MyStates.WAITING_NAME))
async def get_name(msg: Main_Update, fsm: StateInjection):
    name = msg.message.text
    await fsm.set_state(MyStates.WAITING_AGE, data={"name": name})
    await app.send_message_simple(msg.chat_id, f"Hi {name}, now enter your age:")

@app.message(StateFilter(MyStates.WAITING_AGE))
async def finish(msg: Main_Update, fsm: StateInjection):
    age = msg.message.text
    data = await fsm.get_state_Data()
    await fsm.clear_state()
    await app.send_message_simple(msg.chat_id, f"Saved: {data['name']}, age {age}")
```
- 3️⃣ Running Multiple Bots
```python
from Rubika import Bot , MultiRunner , Text , ChatType , Reg ,
Document_Object , Documents , F , StateFilter , state , state_group , StateInjection , Main_Update

bot1 = Bot("TOKEN1")
bot2 = Bot("TOKEN2")

@bot1.message(Text("ping"))
async def pong(msg, fsm):
    await bot1.send_message_simple(msg.chat_id, "pong from bot1")

@bot2.message(Text("ping"))
async def pong2(msg, fsm):
    await bot2.send_message_simple(msg.chat_id, "pong from bot2")

MultiRunner.Run(
    bot1(bot_name="FirstBot"),
    bot2(bot_name="SecondBot")
)
```

## 📚 API Reference
### All methods are inside the Bot class after instantiation.
### Some Method :
- `send_message_simple`
- `send_keypad`
- `send_inline_keypad`
- `send_file`
- `edit_message_text`
- `ban_chat_member`
- `set_commands`

## 🤝 Contributing
### Feel free to open issues or pull requests. Make sure to follow the existing code style and add docstrings for new features.

## 📄 License
### This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

## ⚠️ Disclaimer
### This library is not official and is provided as-is. Rubika’s API may change without notice. The author is not responsible for any misuse.

