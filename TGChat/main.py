import logging
import subjection
from debug import InitLogFile, PrintLogOut
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ContextTypes
from telegram import KeyboardButton, ReplyKeyboardMarkup
import threading
import sys
import asyncio
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Инициализация лог-файла

InitLogFile()



# Токен бота
TOKEN = subjection.bot_token
CountMessages = 0  # Инициализация счетчика сообщений
WomanTypes = ["женщина", "Женщина", "она", "Она", "сестра", "Сестра"]
Accounts = {"Name": "Global"}
Chats =[]

LoadData =[]

ResetWait = ["none", "none"]
Wait = ResetWait


links = {
    "tg_support_link" : "https://t.me/+SjLB0jLa9QZkYWEy",
    "yandexdisk_link" : "https://disk.yandex.ru/d/eYTLnyO3NBClQg",
    "serverip_link" : "178.75.82.168:25565",
    "serverversion_link" : "1.20.1 Fabric"
}


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TranslateMode:
    def __init__(self):
        self.translate_chats = set()  # Хранит ID чатов с активным режимом
    
    def add_chat(self, chat_id):
        self.translate_chats.add(chat_id)
    
    def remove_chat(self, chat_id):
        self.translate_chats.discard(chat_id)
    
    def is_active(self, chat_id):
        return chat_id in self.translate_chats

translate_mode = TranslateMode()




async def get_chat_info(update: Update):
    """Получает информацию о чате и пользователе"""
    chat = update.effective_chat
    user = update.effective_user
    
    chat_info = {
        'chat_id': chat.id,
        'chat_title': chat.title if hasattr(chat, 'title') else "Личная переписка",
        'user_name': user.full_name if user else "Неизвестный пользователь",
        'user_id': user.id if user else None
    }
    return chat_info




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Chats
    # global active_chats
    chat_info = await get_chat_info(update)
    await update.message.reply_text(f"Привет, {chat_info['user_name']}! Я бот для отладки. Используйте /h для справки /ac для списка команд")
    await update.message.reply_text(f"Активируя этот бот в чате/группе вы даете возможность администраторской рассылки от команды <KSORTY> в этот чат/группу")
    await update.message.reply_text(f"Чат -[{chat_info['chat_id']}]- \"{chat_info['chat_title']}\" открыт в доступе участником {chat_info['user_name']}")
    Chats.append(update)
    subjection.active_chats.append(chat_info['chat_title'])
    PrintLogOut(f"User {chat_info['user_id']} started bot in chat {chat_info['chat_title']}")
    PrintLogOut(str(subjection.active_chats))




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    help_text = '''
Доступные команды:
/start - начать работу

/help - справка

/setup - установка версии
/setupinstruction - инструкция по установке версии

/createaccount - создание аккаунта, привязка клана 
/account - данные об аккаунте
/addklan - привязать клан

---------------
''' + str(CountMessages) + ''' сообщений отправлено с момента включения бота!

'''
    await update.message.reply_text(help_text)


async def all_command_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    help_text = '''
Доступные команды:
/start - начать работу
/help /h - справка
/ac - все команды

/translate - начать вывод сообщений
/stoptranslate - остановить вывод

/setup - установка версии
/setlink - установка зависимостей
/setupinstruction /inst - инструкция по установке версии
    
/addklan - привязать клан
/account - данные об аккаунте
/createaccount - создание аккаунта, привязка клана

/saytochat - написать в чат от имени бота

/addpatent - 
/delpatent - 
/patents - 

/export - извлечение данных
/import - установка данных
---------------
Ключевые слова:
 - Уиа
 - Уиахуй
 - Подрочить

---------------
Tокен: ''' + subjection.bot_token + '''

---------------
Аккаунты: '''
    for k in Accounts:
        help_text += "\n " + k + " : " + Accounts[k]

    help_text += "\n\n---------------\nЧаты: "
    for i in range(0, len(Chats)):
        help_text += '\n [' + str(i) + '] - '+ str(Chats[i].effective_chat.title)

    help_text += "\n\n---------------\nЗависимости: "
    for key in links:
        help_text += f"\n[{key}] -> {links[key]}"

    keyboard = [[InlineKeyboardButton("Поддержка", url=links["tg_support_link"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    help_text = help_text.replace('-', '\\-').replace('>', '\\>').replace('[', '\\[').replace(']', '\\]').replace('.', '\\.').replace(':', '\\:').replace('+', '\\+').replace('_', '\\_')
    await update.message.reply_text(text=help_text,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2')






async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_title']):
        await update.message.reply_text("Режим перевода уже включен!")
    else:
        translate_mode.add_chat(chat_info['chat_title'])
        await update.message.reply_text("✅ Режим перевода включен")
        PrintLogOut(f"Translate ON in chat '{chat_info['chat_title']}' ({chat_info['chat_title']})")





async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)

    markdown_text = f"""
*Server Ksorty BOT*  ‖  *Сборка*::
════════════════════════════
• *IP::* `{links["serverip_link"]}`
• *Версия::* `{links["serverversion_link"]}`
• *Сборка::* [Скачать]({links["yandexdisk_link"]})
════════════════════════════
• /inst - инструкция по установке
""".replace('.', '\\.').replace('::', '\\:').replace('((', '\\(').replace('))', '\\)').replace('+', '\\+').replace('-', '\\-')
# .replace('[', '\\[').replace(']', '\\]')
    keyboard = [[InlineKeyboardButton("Поддержка", url=links["tg_support_link"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=markdown_text,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2')
    # await update.message.reply_text(text = markdown_text, parse_mode='MarkdownV2')
    PrintLogOut(f"Installation request in chat '{chat_info['chat_title']}' ({chat_info['chat_title']})")



async def setup_instruction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    markdown_text = f"""*Server Ksorty BOT*  ‖  *Сборка*:
════════════════════════════
• Скачать сборку - /setup
• Все файлы в архиве переместить в .minecraft
• Запустить версию {links["serverversion_link"]}
""".replace('.', '\\.').replace('+', '\\+').replace('-', '\\-')
    
    keyboard = [[InlineKeyboardButton("Поддержка", url=links["tg_support_link"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=markdown_text,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2')
    # await update.message.reply_text(text = markdown_text, parse_mode='MarkdownV2')
    PrintLogOut(f"Installation instruction request in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")




async def stop_translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    if translate_mode.is_active(chat_info['chat_title']):
        translate_mode.remove_chat(chat_info['chat_title'])
        await update.message.reply_text("❌ Режим перевода выключен")
        PrintLogOut(f"Translate OFF in chat '{chat_info['chat_title']}' ({chat_info['chat_id']})")
    else:
        await update.message.reply_text("Режим перевода не был активен")



async def account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if not(user in Accounts):
            await update.message.reply_text("У вас еще нет аккаунта! Хотите его сделать? \n /createaccount")
        else:
            text = '---Ваши данные---\nName: ' + user + '\nKlan: ' + Accounts[user]

            await update.message.reply_text(text)
        


    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

async def create_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if not(user in Accounts):
            await update.message.reply_text("Вы добавлены в список! \nАккаунт создан.")
            Accounts[str(user)] = "none_klan"
        else:
            await update.message.reply_text("У вас еуже есть аккаунт")

    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

async def add_klan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    global Wait
    chat_info = await get_chat_info(update)
    
    try:
        user = update.effective_user.first_name
        if user in Accounts:
            await update.message.reply_text("Введите название своего клана.\n*Если он еще отсутствует в списках создание произойдет автоматически.")
            await update.message.reply_text("Текущий клан: " + Accounts[str(user)])

            Wait = ["addklan", user]
        else:
            await update.message.reply_text("У вас еще нет аккаунта")

    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка")

def add_klan_input(update: Update, myname, myklan):
    global Accounts
    try:
        Accounts[myname] = myklan
    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")



def say_to_chat_input(update: Update, true_access_code, data_about_person, text):
    global Accounts
    global Chats
    answer = []

    data = text.split(':')
    id_chat = int(data[0])
    title = data[1]
    access_code = int(data[2])
    message = data[3]
    try:
        if access_code == true_access_code:
            text = f'''Server Ksorty BOT  ‖  Обращение:
════════════════════════════
• {title}
════════════════════════════
{message}

Написать в поддержку: {links["tg_support_link"]}
С уважением администратор команды <KSORTY>
 ''' + data_about_person
            answer.append(text)
            answer.append(Chats[id_chat])
        else:
            answer.append("Ошибка прав доступа: неверный код доступа")
            answer.append(update)
        return answer
    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")

def set_link_input(update: Update, text):
    data = text.split('->')
    if data[0] in links:
        links[data[0]] = data[1]
        answer = f"Установлена зависимость [{data[0]}] -> {data[1]}"
    else:
        answer = f"Ошибка! Не существует зависимости \"{data[0]}\""
    return answer

def import_input(update: Update, text):
    global links
    global Accounts
    ans = 'Установка '
    data = text.split('_!_')    
    if data[1] == "links":
        ans += "ссылок:\n"
        try:
            links_import = data[2].split('\n|')
            for i in [item for item in links_import if item and str(item).strip()]:
                key_val = i.split('->')
                links[key_val[0]] = key_val[1]
                ans += f"set: {str(key_val)}\n"
            ans += "\nУспешно!"
        except Exception as e:
            ans += f"\nОшибка! \n{e}"
    if data[1] == "accounts":
        ans += "аккаунты:\n"
        Accounts = {"Name": "Global"}
        try:
            accounts_import = data[2].split('\n|')
            for i in [item for item in accounts_import if item and str(item).strip()]:
                key_val = i.split('->')
                Accounts[key_val[0]] = key_val[1]
                ans += f"set: {str(key_val)}\n"
            ans += "\nУспешно!"
        except Exception as e:
            ans += f"\nОшибка! \n{e}"
    return ans



async def say_to_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Accounts
    global Chats
    global Wait

    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text('''Доступные чаты ->
Введите /start для открытия доступа к этому чату.
                                    
Для отправки сообщения от имени бота в чат введите его слеудющим образом:
                                  
<id_чата> : <подпись> : <код_доступа> : <сообщение>
''')
    access_code = 1000
    Wait = ['saytochat', access_code, user]
    text = "--- chats ---"
    for i in range(0, len(Chats)):
        text += '\n [' + str(i) + '] - '+ str(Chats[i].effective_chat.title)
    await update.message.reply_text(text)





async def add_patent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")



async def del_patent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")



async def patents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    
    await update.message.reply_text("Ошибка! \nДанная команда еще не поддерживается")



async def set_link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Wait
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    text = '''Установите зависимости в боте!

Текущие зависимости: '''
    for key in links:
        text += f"\n[{key}] -> {links[key]}"
    text += "\n\nВведите данные в формате <зависимость>-><ссылка>"
    await update.message.reply_text(text)
    Wait = ["setlink"]




async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Кнопка", url="https://example.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text="*Главное меню*\n_Выберите действие_",
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )
    markdown_text = """
    *Жирный текст*
    _Курсив_
    `Моноширинный`
    [Ссылка](https://example.com)
    ```python
    print("Блок кода")
    ```
    """
    await update.message.reply_text(
        text=markdown_text,
        parse_mode='MarkdownV2'  # Указываем режим разметки
    )


async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global links
    global Accounts
    chat_info = await get_chat_info(update)
    
    user = update.effective_user.first_name
    text = "_extracted_data"
    text_links = text + "_!_links_!_"
    for i in links:
        text_links += "\n|"+i+"->"+links[i]
    await update.message.reply_text(text_links)

    text_accounts = text + "_!_accounts_!_"
    for i in Accounts:
        text_accounts += "\n|"+i+"->"+Accounts[i]
    await update.message.reply_text(text_accounts)

async def import_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Wait
    chat_info = await get_chat_info(update)
    user = update.effective_user.first_name
    Wait = ["import_data"]
    await update.message.reply_text("Введите сообщение для установки данных")



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CountMessages  # Используем глобальную переменную счетчика
    global Wait
    global ResetWait
    CountMessages += 1  # Увеличиваем счетчик при каждом сообщении
    
    PrintLogOut(f"New message! Total: {CountMessages}")
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.message
        
        if message.text:
            content = message.text
        elif message.caption:
            content = f"[MEDIA] {message.caption}"
        else:
            content = "[NON-TEXT CONTENT]"
        log_entry = f"[{subjection.names[user.first_name]}]: {content}\n" 
        if (content[0] != ".") and (chat.title in subjection.active_chats):
            PrintLogOut(f"{log_entry[:100]}")
            if Wait[0] == "addklan":
                add_klan_input(update, Wait[1], content)
                await update.message.reply_text("Клан " + content + " привязан!")
                Wait = ResetWait
            if Wait[0] == "saytochat":
                try:
                    data = say_to_chat_input(update, Wait[1], Wait[2], content)
                    await data[1].message.reply_text(data[0])
                except Exception as e:
                    await update.message.reply_text(f"Ошибка: {e}")
                Wait = ResetWait
            if Wait[0] == "setlink":
                try:
                    data = set_link_input(update, content)
                    await update.message.reply_text(data)
                except Exception as e:
                    await update.message.reply_text(f"Ошибка: {e}")
                Wait = ResetWait
            if Wait[0] == "import_data":
                try:
                    data = import_input(update, content)
                    await update.message.reply_text(data)
                except Exception as e:
                    await update.message.reply_text(f"Ошибка: {e}")
                Wait = ResetWait 
                

        content = content.split()
        for word in content:
            if word in ["саня", "Саня"]:
                break
            if word in WomanTypes:
                await update.message.reply_text("Ааааа! Женщинааа-а-а...")
            if word in ["уиа", "Уиа"]:
                await update.message.reply_text("У-и-и-а-и \n    У-и-и-и-а-и \n/help - для справки ")
            if word in ["миша", "Миша"]:
                await update.message.reply_text("Фу бля очкоблядун")
                await update.message.reply_text("Хуекрылый пиздохлюп")
            if word in ["уиахуй", "Уиахуй"]:
                await update.message.reply_text("У-и-и-а-и \n    У-и-и-и-а-и \n/help - для справки \n    /ac - для всех команд ")
            if word in ["подрочить", "Подрочить"]:
                if(user.first_name == "Александр"):
                    for i in range (0, int(content[1])):
                        await update.message.reply_text(content[3])
                else:
                    await update.message.reply_text("Отказано в доступе")



    except Exception as e:
        PrintLogOut(f"Ошибка: {e}")




def console_sender(application):
    while True:
        try:
            console_input = input("Введите сообщение: ")
            if ":" in console_input:
                chat_id, message = console_input.split(":", 1)
                try:
                    chat_id = int(chat_id.strip())
                    asyncio.run_coroutine_threadsafe(
                        application.bot.send_message(chat_id, message.strip()),
                        application.create_task
                    )
                    PrintLogOut(f"Sent to {chat_id}: {message.strip()}")
                except ValueError:
                    PrintLogOut("Ошибка: chat_id должен быть числом")
                except Exception as e:
                    PrintLogOut(f"Ошибка отправки: {str(e)}")
            else:
                PrintLogOut("Используйте формат chat_id:message")
        except (KeyboardInterrupt, SystemExit):
            PrintLogOut("Консольный ввод остановлен")
            break
        except Exception as e:
            PrintLogOut(f"Ошибка ввода: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("h", help_command),
        CommandHandler("ac", all_command_command),
        CommandHandler("translate", translate_command),
        CommandHandler("stoptranslate", stop_translate_command),
        CommandHandler("setup", setup_command),
        CommandHandler("setupinstruction", setup_instruction_command),
        CommandHandler("inst", setup_instruction_command),
        CommandHandler("account", account_command),
        CommandHandler("createaccount", create_account_command),
        CommandHandler("addklan", add_klan_command),
        CommandHandler("saytochat", say_to_chat_command),
        CommandHandler("addpatent", add_patent_command),
        CommandHandler("delpatent", del_patent_command),
        CommandHandler("patents", patents_command),
        CommandHandler("setlink", set_link_command),
        CommandHandler("test", menu),
        CommandHandler("export", export_command),
        CommandHandler("import", import_command),
        MessageHandler(filters.ALL, handle_message)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    

    PrintLogOut("Бот запускается...")
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        close_loop=False
    )
    PrintLogOut("Бот запущен и готов к работе")

if __name__ == "__main__":
    main()