import requests
import time


from bs4 import BeautifulSoup 
from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from unicode_converter import converter   
from href_creation import  UserHREF, users, href, href_for_parser


filials = ['Уфа', 'Стерлитамак', 'Салават', 'Октябрьский', 'Отмена']
learn_types = ['Очная', 'Очно-заочная', 'Заочная']
fakults = ['УВШЭУ', 'IT-институт', 'ВыШкаИнСоТех', 'ТФ', 'ИЭС', 'ИНИЦТ', 'ИНБ', 'ГНФ', 'АСИ', 'ФТТ', 'ОКТФЛ', 'ЦПК', 'CЛФЛ', 'СТФЛ' 'Отмена']
courses = ['1', '2', '3', '4', 'Отмена']
semmesters = ['Весенний', 'Осенний', 'Отмена']
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Отмена']


class Schedule(StatesGroup):
    waitin_for_fil_name = State()
    waitin_for_learntype_name = State()
    waitin_for_fakult_name = State()
    waitin_for_course_name = State()
    waitin_for_sem_name = State()
    waitin_for_group_name = State()
    waitin_for_parser = State()


async def schedule_start(message: types.Message):
    global users 
    users = UserHREF(message.from_user.id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for filial in filials:
        keyboard.add(filial)
    
    await message.answer_sticker(r'CAACAgIAAxkBAAED7wpiC291pgn8Fdju14mXdm911Jvc7AACVAADQbVWDGq3-McIjQH6IwQ')
    await message.answer(f'Привет, {message.from_user.first_name} если понадобиться помощь используй комнаду /help, также ты можешь ореинтироваться с помощью меню ниже! \nДля начала, выбери филиал используя кнопки', reply_markup=keyboard)

    await Schedule.waitin_for_fil_name.set()

async def filial_chosen(message: types.Message, state: FSMContext):
    if message.text not in filials:
        await message.answer('Пожалуйста, выберите филиал, используя кнопки')
        return
    await state.update_data(chosen_filial = message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for learn_type in learn_types:
        keyboard.add(learn_type)
    await message.answer('Теперь - форму обучения', reply_markup=keyboard)
    await Schedule.next()

async def learn_type_chosen(message: types.Message, state:FSMContext):
    if message.text not in learn_types:
        await message.answer('Пожалуйста, выберите форму обучения, используя кнопки')
        return
    await state.update_data(learn_type = message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for fakult in fakults:
        keyboard.add(fakult)
    await Schedule.next()
    await message.answer('Понял тебя, а в каком факультете ты учишься?', reply_markup=keyboard)

async def fakult_chosen(message: types.Message, state: FSMContext):
    if message.text not in fakults:
        await message.answer('Пожалуйста, выберите факультет, используя кнопки')
        return
    await state.update_data(fakult = message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for course in courses:
        keyboard.add(course)
    await Schedule.next()
    await message.answer('На каком курсе учишься?', reply_markup=keyboard)

async def course_chosen(message: types.Message, state: FSMContext):
    if message.text not in courses:
        await message.text('Пажалуйста, выбери курс, используя кнопки')
        return 
    await state.update_data(course = message.text)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for sem in semmesters:
        keyboard.add(sem)
    await Schedule.next()
    await message.answer('Напомни пожалуйста, какой сейчас семместр?', reply_markup=keyboard)

async def sem_chosen(message: types.Message, state: FSMContext):
    if message.text not in semmesters:
        await message.answer('Пожалуйста, выбери семместр, используя кнопки')
        return 
    await state.update_data(semmester = message.text)

    
    await Schedule.next()
    await message.answer('Почти готово! Осталось ввести свою группу. Пример ГРУППА-17-01')

text_mon = {}; text_tue = {}; text_wed = {}; text_thr = {}; text_fri = {}; text_sat = {}
page = ''
user_data = ''; href = {}
async def group_name_entered(message: types.Message, state:FSMContext):
    global href
    global users


    await message.answer('Загрузка расписания...')
    #group_nam = message.text
    #await state.update_data(group_name = group_nam)
    user_data = await state.get_data()

    if user_data['chosen_filial'] == 'Уфа':
        users.set_href(message.from_user.id, 'fil', '1')
    elif user_data['chosen_filial'] == 'Октябрьский':
        users.set_href(message.from_user.id, 'fil', '2')
    elif user_data['chosen_filial'] == 'Салават':
        users.set_href(message.from_user.id, 'fil', '3')
    elif user_data['chosen_filial'] == 'Стерлитамак':
        users.set_href(message.from_user.id, 'fil', '4')

    if user_data['learn_type'] == 'Очная':
        users.set_href(message.from_user.id, 'fob', '1')
    elif user_data['learn_type'] == 'Очно-заочная':
        users.set_href(message.from_user.id, 'fob', '2')
    elif user_data['learn_type'] == 'Заочная':
        users.set_href(message.from_user.id, 'fob', '3')

    if user_data['fakult'] == 'ФТТ':
        users.set_href(message.from_user.id, 'fak', '7')
    elif user_data['fakult'] == 'АСИ':
        users.set_href(message.from_user.id, 'fak', '17')
    elif user_data['fakult'] == 'ЦПК':
        users.set_href(message.from_user.id, 'fak', '28')
    elif user_data['fakult'] == 'ГНФ':
        users.set_href(message.from_user.id, 'fak', '1')
    elif user_data['fakult'] == 'ИНБ':
        users.set_href(message.from_user.id, 'fak', '16')
    elif user_data['fakult'] == 'ИНИЦТ':
        users.set_href(message.from_user.id, 'fak', '30')
    elif user_data['fakult'] == 'ИЭС':
        users.set_href(message.from_user.id, 'fak', '19')
    elif user_data['fakult'] == 'ТФ':
        users.set_href(message.from_user.id, 'fak', '3')
    elif user_data['fakult'] == 'УВШЭУ':
        users.set_href(message.from_user.id, 'fak', '22')
    elif user_data['fakult'] == 'IT-институт':
        users.set_href(message.from_user.id, 'fak', '23')
    elif user_data['fakult'] == 'ВыШкаИнСоТех':
        users.set_href(message.from_user.id, 'fak', '24')
    
    users.set_href(message.from_user.id, 'kurs', user_data['course'])

    if user_data['semmester'] == 'Весенний':
        users.set_href(message.from_user.id, 'sem', '0')
    elif user_data['semmester'] == 'Осенний':
        users.set_href(message.from_user.id, 'sem', '1')

    href_for_parser[message.from_user.id] = {}

    group_name_eng = ['BME02', 'BME01', 'BPT01', 'BPT02']
    group_href = []; nums = ['0','1','2','3','4','5','6','7','8','9']

    group_nam = message.text
    group_name = group_nam[:-6]
    group_index = group_nam[len(group_name):]
    if group_name in group_name_eng:
        group_href.append(group_name); group_href.append(group_index)
        users.set_href(message.from_user.id, 'gruppa', ''.join(group_href))
    else:
        for i in group_name:
            if i in nums:
                group_href.append(i)
            else:
                group_href.append(converter(i)) 
        group_href.append(group_index)
        users.set_href(message.from_user.id, 'gruppa', ''.join(group_href))

    users.get_existed_href(message.from_user.id)

    global text_mon 
    global text_tue
    global text_wed
    global text_thr 
    global text_fri 
    global text_sat 
    text_mon[message.from_user.id] = {}; text_tue[message.from_user.id] = {}; text_wed[message.from_user.id] = {}; text_thr[message.from_user.id] = {}; text_fri[message.from_user.id] = {}; text_sat[message.from_user.id] = {}


    page = requests.get(href_for_parser[message.from_user.id]['href'])
    soup = BeautifulSoup(page.content, 'lxml')

    class Monday:
        mon1 = soup.find("th").find_parent("tr").find_next("tr") 
        mon2 = mon1.find_next("tr")
        mon3 = mon2.find_next("tr")
        mon4 = mon3.find_next("tr")
        mon5 = mon4.find_next("tr")
        mon6 = mon5.find_next("tr")
        mon7 = mon6.find_next("tr")

    class Tuesday:
        tue1 = Monday.mon7.find_next("tr")
        tue2 = tue1.find_next("tr")
        tue3 = tue2.find_next("tr")
        tue4 = tue3.find_next("tr")
        tue5 = tue4.find_next("tr")
        tue6 = tue5.find_next("tr")
        tue7 = tue6.find_next("tr")

    class Wednesday:
        wed1 = Tuesday.tue7.find_next("tr")
        wed2 = wed1.find_next("tr")
        wed3 = wed2.find_next("tr")
        wed4 = wed3.find_next("tr")
        wed5 = wed4.find_next("tr")
        wed6 = wed5.find_next("tr")
        wed7 = wed6.find_next("tr")

    class Thursday: 
        thr1 = Wednesday.wed7.find_next("tr")
        thr2 = thr1.find_next("tr")
        thr3 = thr2.find_next("tr")
        thr4 = thr3.find_next("tr")
        thr5 = thr4.find_next("tr")
        thr6 = thr5.find_next("tr")
        thr7 = thr6.find_next("tr")

    class Friday:
        fri1 = Thursday.thr7.find_next("tr")
        fri2 = fri1.find_next("tr")
        fri3 = fri2.find_next("tr")
        fri4 = fri3.find_next("tr")
        fri5 = fri4.find_next("tr")
        fri6 = fri5.find_next("tr")
        fri7 = fri6.find_next("tr")

    class Saturday:
        sat1 = Friday.fri7.find_next("tr")
        sat2 = sat1.find_next("tr")
        sat3 = sat2.find_next("tr")
        sat4 = sat3.find_next("tr")
        sat5 = sat4.find_next("tr")
        sat6 = sat5.find_next("tr")
        sat7 = sat6.find_next("tr")

    block_mon = {'1. 8:45 - 10:20': Monday.mon1.find_all("b"), '2. 10:30 - 12:05': Monday.mon2.find_all("b"), '3. 12:15 - 13:50': Monday.mon3.find_all("b"),\
    '4. 14:35 - 16:10': Monday.mon4.find_all("b"), '5. 16:20 - 17:55': Monday.mon5.find_all("b"), '6. 18:05 - 19:40': Monday.mon6.find_all("b"),\
        '7  19:50 - 21:15': Monday.mon7.find_all("b")}

    block_tue = {'1. 8:45 - 10:20': Tuesday.tue1.find_all("b"), '2. 10:30 - 12:05': Tuesday.tue2.find_all("b"), '3. 12:15 - 13:50': Tuesday.tue3.find_all("b"),\
    '4. 14:35 - 16:10': Tuesday.tue4.find_all("b"), '5. 16:20 - 17:55': Tuesday.tue5.find_all("b"), '6. 18:05 - 19:40': Tuesday.tue6.find_all("b"),\
        '7  19:50 - 21:15': Tuesday.tue7.find_all("b")}

    block_wed = {'1. 8:45 - 10:20': Wednesday.wed1.find_all("b"), '2. 10:30 - 12:05': Wednesday.wed2.find_all("b"), '3. 12:15 - 13:50': Wednesday.wed3.find_all("b"),\
    '4. 14:35 - 16:10': Wednesday.wed4.find_all("b"), '5. 16:20 - 17:55': Wednesday.wed5.find_all("b"), '6. 18:05 - 19:40': Wednesday.wed6.find_all("b"),\
        '7  19:50 - 21:15': Wednesday.wed7.find_all("b")}

    block_thr = {'1. 8:45 - 10:20': Thursday.thr1.find_all("b"), '2. 10:30 - 12:05': Thursday.thr2.find_all("b"), '3. 12:15 - 13:50': Thursday.thr3.find_all("b"),\
    '4. 14:35 - 16:10': Thursday.thr4.find_all("b"), '5. 16:20 - 17:55': Thursday.thr5.find_all("b"), '6. 18:05 - 19:40': Thursday.thr6.find_all("b"),\
        '7  19:50 - 21:15': Thursday.thr7.find_all("b")}

    block_fri = {'1. 8:45 - 10:20': Friday.fri1.find_all("b"), '2. 10:30 - 12:05': Friday.fri2.find_all("b"), '3. 12:15 - 13:50': Friday.fri3.find_all("b"),\
    '4. 14:35 - 16:10': Friday.fri4.find_all("b"), '5. 16:20 - 17:55': Friday.fri5.find_all("b"), '6. 18:05 - 19:40': Friday.fri6.find_all("b"),\
        '7  19:50 - 21:15': Friday.fri7.find_all("b")}

    block_sat = {'1. 8:45 - 10:20': Saturday.sat1.find_all("b"), '2. 10:30 - 12:05': Saturday.sat2.find_all("b"), '3. 12:15 - 13:50': Saturday.sat3.find_all("b"),\
    '4. 14:35 - 16:10': Saturday.sat4.find_all("b"), '5. 16:20 - 17:55': Saturday.sat5.find_all("b"), '6. 18:05 - 19:40': Saturday.sat6.find_all("b"),\
        '7  19:50 - 21:15': Saturday.sat7.find_all("b")}
    
    def get_days_final(block):
        time = ['1. 8:45 - 10:20', '2. 10:30 - 12:05', '3. 12:15 - 13:50', '4. 14:35 - 16:10', '5. 16:20 - 17:55', '6. 18:05 - 19:40', '7  19:50 - 21:15']
        ans = []
        for i in range(7):
            rob = block[time[i]]
            if rob != []:
                ans.append(time[i])
                #ans.append(' ')
                for j in range(len(rob)):
                    if j+1 == len(rob) and j != 0:
                        s = ''; cnt = 0; arr = str(rob[j])[4:-4]
                        for i in range(len(arr)):
                            if arr[i] == ' ':
                                cnt += 1
                            if cnt == 3:
                                s = arr[i+1:]
                                break 
                        ans.append(s)
                        ans.append('')
                    elif len(rob) == 1:
                        s = ''; cnt = 0; arr = str(rob[j])[4:-4]
                        for i in range(len(arr)):
                            if arr[i] == ' ':
                                cnt += 1
                            if cnt == 3:
                                s = arr[i+1:]
                                break 
                        ans.append(s)
                        ans.append('')
                    else:
                        s = ''; cnt = 0; arr = str(rob[j])[4:-4]
                        for i in range(len(arr)):
                            if arr[i] == ' ':
                                cnt += 1
                            if cnt == 3:
                                s = arr[i+1:]
                                break 
                        ans.append(s)

                    #ans.append(f'{time[i]} {rob[j]}')
        ans.append('Ссылка в ЛК - https://ams.rusoil.net/pcs/')
        return ans
    
    text_mon[message.from_user.id]['mon'] = '\n'.join(get_days_final(block_mon))
    text_tue[message.from_user.id]['tue'] = '\n'.join(get_days_final(block_tue))
    text_wed[message.from_user.id]['wed'] = '\n'.join(get_days_final(block_wed))
    text_thr[message.from_user.id]['thr'] = '\n'.join(get_days_final(block_thr))
    text_fri[message.from_user.id]['fri'] = '\n'.join(get_days_final(block_fri))
    text_sat[message.from_user.id]['sat'] = '\n'.join(get_days_final(block_sat))

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for day in days:
        keyboard.add(day)
    
    await message.answer('Теперь - выбери расписание', reply_markup=keyboard)
    
    await Schedule.next()

async def parser_ready(message: types.Message, state: FSMContext):
    if message.text not in days:
        await message.answer('Пожалуйста, выберите дни, используя кнопки')
        return
    
    global text_mon 
    global text_tue
    global text_wed
    global text_thr 
    global text_fri 
    global text_sat 

    day_name = message.text
    if day_name == 'Понедельник':
        text_final = len(text_mon[message.from_user.id]['mon'])
        if text_final > 100:
            await message.answer(text_mon[message.from_user.id]['mon'])
        else:
            await message.answer('В понедельник нет занятий')
    elif day_name == 'Вторник':
        text_final = len(text_tue[message.from_user.id]['tue'])
        if text_final > 100:
            await message.answer(text_tue[message.from_user.id]['tue'])
        else:
            await message.answer('Во вторник нет занятий')
    elif day_name == 'Среда':
        text_final = len(text_wed[message.from_user.id]['wed'])
        if text_final > 100:
            await message.answer(text_wed[message.from_user.id]['wed'])
        else:
            await message.answer('В среду нет занятий')
    elif day_name == 'Четверг':
        text_final = len(text_thr[message.from_user.id]['thr'])
        if text_final > 100:
            await message.answer(text_thr[message.from_user.id]['thr'])
        else:
            await message.answer('В четверг нет занятий')
    elif day_name == 'Пятница':
        text_final = len(text_fri[message.from_user.id]['fri'])
        if text_final > 100:
            await message.answer(text_fri[message.from_user.id]['fri'])
        else:
            await message.answer('В пятницу нет занятий')
    elif day_name == 'Суббота':  
        text_final = len(text_sat[message.from_user.id]['sat'])
        if text_final > 100:    
            await message.answer(text_sat[message.from_user.id]['sat'])
        else:
            await message.answer('В субботу нет занятий')

    #await state.reset_state(with_data=False)


async def notify(message: types.Message):
    await message.answer('В разраотке...')
    
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(schedule_start, commands="start", state = "*")
    dp.register_message_handler(notify, commands="notify", state="*")
    dp.register_message_handler(filial_chosen, state=Schedule.waitin_for_fil_name)
    dp.register_message_handler(learn_type_chosen, state=Schedule.waitin_for_learntype_name)
    dp.register_message_handler(fakult_chosen, state=Schedule.waitin_for_fakult_name)
    dp.register_message_handler(course_chosen, state=Schedule.waitin_for_course_name)
    dp.register_message_handler(sem_chosen, state=Schedule.waitin_for_sem_name)
    dp.register_message_handler(group_name_entered, state=Schedule.waitin_for_group_name)
    dp.register_message_handler(parser_ready, state=Schedule.waitin_for_parser)