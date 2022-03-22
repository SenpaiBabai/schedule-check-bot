from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def cmd_cancel(message: types.Message, state:FSMContext):
    await state.finish()
    await message.answer('Ваша настройка бота сброшена! Вы можете ореинтироваться с помощью меню ниже,\nнажмите /start для перезапуска бота и настройки расписания', reply_markup=types.ReplyKeyboardRemove())
    await message.answer_sticker(r'CAACAgIAAxkBAAED7xpiC3NnyR028hwAAT0uza7ch468CYgAAoEBAAIrXlMLXgpsPmwAAXi0IwQ')

async def cmd_help(message: types.Message):
    await message.answer('У тебя на вооружении всего 3 команды:\n/start - перезапускает бота\n/cancel - сбрасывает настройку бота\n/help - выводит это сообщение\nПо всем вопросам или ошибкам писать сюда -> @SenpaiBabai')



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")