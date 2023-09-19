import telebot
from telebot import types
import datetime
import json
import pytz  

moscow_tz = pytz.timezone('Europe/Moscow')
bot = telebot.TeleBot(' ')

# JSON
def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка при декодировании JSON в файле {filename}.")
        return None

def get_moscow_time():
    return datetime.datetime.now(moscow_tz)

nowDay = get_moscow_time().weekday()
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
nowDay = days_of_week[nowDay]

# временная конструкция определения следующего дня
nextDay = "none"
if nowDay == "Понедельник":
    nextDay = "Вторник"
elif nowDay == "Вторник":
    nextDay = "Среда"
elif nowDay == "Среда":
    nextDay = "Четверг"
elif nowDay == "Четверг":
    nextDay = "Пятница"
elif nowDay == "Пятница":
    nextDay = "Суббота"
elif nowDay == "Суббота":
    nextDay = "Воскресенье"
elif nowDay == "Воскресенье":
    nextDay = "Понедельник"

current_date = get_moscow_time()
week_number = current_date.isocalendar()[1]
if week_number % 2 == 0:
    nowParity = "Четная неделя"
else:
    nowParity = "Нечетная неделя"


@bot.message_handler(content_types=['text'])
def get_text_messages(message):


# Функции для команд

    def backMenu():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        relist = types.KeyboardButton("🗓️ Замены")
        list = types.KeyboardButton("🗓️ Расписание")
        help = types.KeyboardButton("⚠️ Помощь")
        settings = types.KeyboardButton("⚙️ Настройки")
        resources = types.KeyboardButton("🌐 Ресурсы")
        keyboard.add(relist, list, help, resources, settings)
        bot.send_message(message.chat.id, f"""
{message.from_user.username}, Привет! Навигация по боту:
🗓️ Замены - список замен
🗓️ Расписание - расписание на день
⚠️ Помощь - помощь по боту
⚙️ Настройки - настройки бота

🔔 Рекомендуется подписаться на уведомления в меню настроек
""", reply_markup=keyboard)
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /start")
        

    def sendNotifi(notificationMessage):
    # Открываем файл JSON для чтения
        with open("users.json", "r") as file:
            data = json.load(file)  # Загружаем данные из файла
            users = data.get("notifications", [])  # Получаем список пользователей из файла

            # Отправляем уведомление каждому пользователю
            for user in users:
                user_id = user.get("uID")
                message_text = notificationMessage
                bot.send_message(user_id, message_text)
# Команды


    if message.text == "/getid":
        bot.send_message(message.chat.id, f"{message.from_user.username}, ID чата: {message.chat.id}")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /getid")

    elif message.text == "/qbezka":
        sendNotifi(notificationMessage="🔔 Работа бота в чатах остановлена. Обращайтесь к боту в личку (сюда): t.me/mgkeitIP_bot")

    if message.chat.id < 0:
        bot.send_message(message.chat.id, "😢 Бот не работает в группах\nРабота с ботом в личке: @mgkeitIP_bot")

    else:

        if message.text == "/start":
            backMenu()

        elif message.text == "🗓️ Расписание":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            today = types.KeyboardButton("📅 Сегодня")
            nextday = types.KeyboardButton("➡️ Завтра")
            skipList = types.KeyboardButton("")
            backList = types.KeyboardButton("🔙 Назад")
            keyboard.add(today, nextday, skipList, backList)
            bot.send_message(message.chat.id, f"{message.from_user.username}, выбери дату, на которую хочешь получить расписание", reply_markup=keyboard)

        elif message.text == "📅 Сегодня":
            filename = "couples.json"
            parsed_data = read_json_file(filename)
            if parsed_data:
                try:
                    monday_schedule = parsed_data[nowParity][nowDay]
                    text_schedule = ""
                    for key, value in monday_schedule.items():
                        text_schedule += f"{key}: {value}\n"
                    bot.send_message(message.chat.id, f"{message.from_user.username}, Расписание на {nowDay} ({nowParity}):\n\n{text_schedule}")
                    print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Расписание")
                except KeyError:
                    print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")
                    print(f"[{datetime.datetime.now()}] Данные о расписании на день не были получены, ошибка")

        elif message.text == "➡️ Завтра":
            filename = "couples.json"
            parsed_data = read_json_file(filename)
            if parsed_data:
                try:
                    monday_schedule = parsed_data[nowParity][nextDay]
                    text_schedule = ""
                    for key, value in monday_schedule.items():
                        text_schedule += f"{key}: {value}\n"
                    bot.send_message(message.chat.id, f"{message.from_user.username}, Расписание на {nextDay} ({nowParity}):\n\n{text_schedule}")
                    print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Расписание")
                except KeyError:
                    print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")
                    print(f"[{datetime.datetime.now()}] Данные о расписании на день не были получены, ошибка")

        elif message.text == "🔙 Назад":
            backMenu()

        elif message.text == "🗓️ Замены":
            bot.send_message(message.chat.id, f"{message.from_user.username}, Список замен на {nowDay}:\n- Сегодня замен нет")
            print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")

        elif message.text == "⚠️ Помощь":
            bot.send_message(message.chat.id, f"{message.from_user.username}, Бот создан для группы 1ИП-4-23\nСписок основных возможностей:\n- Просмотр расписания на текущий день.\n- Просмотр замен на текущий день.\n- Просмотр основной информации на день.")
            print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Помощь")

        elif message.text == "🌐 Ресурсы":
            bot.send_message(message.chat.id, f"{message.from_user.username}, ресурсы:\n- Навигатор студента: sites.google.com/view/mgkeitstudent/\n- ВКонтакте: vk.com/mgkeit1\n- Телеграм: t.me/mgkeit\n- Работа от МГКЭИТ: t.me/VacanciMGKEIT\n\nСвязь с разработчиком: @shzpard")
        
        elif message.text == "⚙️ Настройки":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            notifiOn = types.KeyboardButton("🔔 Уведомления (ON)")
            notifiOff = types.KeyboardButton("🔕 Уведомления (OFF)")
            skipList = types.KeyboardButton("")
            backList = types.KeyboardButton("🔙 Назад")
            keyboard.add(notifiOn, notifiOff, skipList, backList)
            bot.send_message(message.chat.id, f"🔔 Здесь можно управлять уведомлениями и рассылками", reply_markup=keyboard)  

        elif message.text == "🔔 Уведомления (ON)":
            user_id = message.from_user.id
            user_data = {"uID": user_id}
            with open("users.json", "r+") as file:
                data = json.load(file)
                users = data.get("notifications", [])

                if user_id not in [user.get("uID") for user in users]:
                    users.append(user_data)
                    data["notifications"] = users
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    bot.send_message(message.chat.id, "🔔 Подписка на уведомления оформлена")

        elif message.text == "🔕 Уведомления (OFF)":
            with open("users.json", "r+") as file:
                user_id = message.from_user.id
                data = json.load(file)
                users = data.get("notifications", [])
                if user_id in [user.get("uID") for user in users]:
                    users = [user for user in users if user.get("uID") != user_id] 
                    data["notifications"] = users 
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    bot.send_message(message.chat.id, "🔕 Ты успешно отписался от уведомлений!")




bot.polling(none_stop=True, interval=0)
