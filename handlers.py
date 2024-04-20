from aiogram import types, F, Router, flags, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message,
)
from aiogram.fsm.state import State, StatesGroup

import text
import kb
from data_base.postgr_sql_base import SQL_request  

router = Router()

class SaveMessage(StatesGroup):
    waiting_for_message = State()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.generate_menu(level='0').as_markup())
    await msg.delete()

@router.callback_query(lambda callback: callback.data == "registr")
async def register_handler(callback: CallbackQuery):
    
    ret = SQL_request().register_user(username=msg.from_user.full_name, telgram_id=msg.from_user.id)
    await callback.message.answer('Test', reply_markup=kb.generate_menu(level='2.1').as_markup())
    await callback.message.delete()

@router.callback_query(lambda callback: callback.data == "train_edit")
async def train_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SaveMessage.waiting_for_message)
    await callback.message.answer(text.menu_train_edit, reply_markup=kb.generate_menu(level='1').as_markup())
    await callback.message.delete()

@router.callback_query(lambda callback: callback.data == "add_train")
async def add_handler(callback: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    if 'saved_message' in data:
        #ret = SQL_request().add_train(text=data['saved_message'], telegram_id=callback.message.from_user.id)
        await callback.message.answer('Test', reply_markup=kb.generate_menu(level='2.1').as_markup())
        
    else:
        await callback.message.answer("Вы ничего не добавляли!\nПопробуйте еще раз", reply_markup=kb.generate_menu(level='2.1').as_markup())
    await state.clear()
    await callback.message.delete()
    
    
        
@router.callback_query(lambda callback: callback.data == "del_train")
async def del_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'saved_message' in data:
        #ret = SQL_request().del_train(text=data['saved_message'], telegram_id=callback.message.from_user.id)
        await callback.message.answer('Test', reply_markup=kb.generate_menu(level='2.1').as_markup())
        
    else:
        await callback.message.answer("Вы ничего не добавляли!\nПопробуйте еще раз", reply_markup=kb.generate_menu(level='2.1').as_markup())
    await state.clear()
    await callback.message.delete()   
    
@router.message(Command("doc"))
async def doc_handler(msg: Message):
    print(msg.text)
    SQL_request().doc_gen()
    await msg.send('log.xlsx')
    
@router.message(Command("dev_info"))
async def dev_request(msg: Message):
    print(msg.text)
    t = msg.text
    t = t.split(' ;')[1].split(';')
    ret = SQL_request().request_dev(req=t[0], password=t[1])
    await msg.reply(ret)  
    
    
@router.message(SaveMessage.waiting_for_message)
async def save_message(message: Message, state: FSMContext):
    data = await state.get_data()
    data['saved_message'] = message.text
    await state.update_data(data)
    await message.delete()
    
@router.callback_query(lambda callback: callback.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.message.answer(text.greet, reply_markup=kb.generate_menu(level='0').as_markup())
    await callback.message.delete()