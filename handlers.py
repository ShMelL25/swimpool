from aiogram import types, F, Router, flags, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import text

from data_base.postgr_sql_base import SQL_request  

router = Router()


@router.message(F.text == "Привет!")
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name))

@router.message(F.text == "Регистрация")
@router.message(Command("registration"))
async def register_handler(msg: Message):
    
    ret = SQL_request().register_user(username=msg.from_user.full_name, telgram_id=msg.from_user.id)
    await msg.reply(ret)  


@router.message(Command("add"))
async def add_handler(msg: Message):
    print(msg.text)
    ret = SQL_request().add_train(text=msg.text, telegram_id=msg.from_user.id)
    await msg.reply(ret)  
    
        
@router.message(Command("del"))
async def del_handler(msg: Message):
    print(msg.text)
    ret = SQL_request().del_train(text=msg.text, telegram_id=msg.from_user.id)
    await msg.reply(ret)   