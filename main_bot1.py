# -*- coding: utf8 -*-
import telebot;
import teletoken;
import constants;
import time;
import logging
from flask import Flask, request
from telebot import types
import json
import requests
#from likes import *
#import mysql_bot;

BOT_URL = 'https://api.telegram.org/bot'+teletoken.token+'/'
# our telegram bot
bot = telebot.TeleBot(teletoken.token);

# настройки для журнала
logger = logging.getLogger('log')
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('ckbi_botic.log')
logger.addHandler(fh)
formatter = logging.Formatter("%(asctime)s  |  %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)

teleuser = 'unknown user';  # пользователь telegram
user_id = 0;  # Пользователь ЦК BI
cx_error = "";
ucode = True;


print("БОТИК ЦК BI - СОБРАНИЕ ЦК")

#dbmsql = mysql_bot.db_mysql(logger);
#dbmsql.connect();
#db_chat = mysql_bot.db_chat(logger, dbmsql);
#db_ques = mysql_bot.db_questions(logger, dbmsql);
#db_ques.load();
#db_subj = mysql_bot.db_subject(logger, dbmsql);

def send_image(p_ChatID, msgtxt, img_file, bPortal=False, Portal=None, Button=telebot.types.ReplyKeyboardMarkup(True, False)):
    try:
        if msgtxt != "":
            if msgtxt is not None:
                bot.send_message(p_ChatID, msgtxt)

        # all_images = os.listdir(constants.dir_image)
        if not bPortal:
            img = open(constants.dir_image + img_file, 'rb')
        else:
            img = open(Portal.GetPhoto(Button), 'rb')

        bot.send_chat_action(p_ChatID, 'upload_photo')
        bot.send_photo(p_ChatID, img)
        img.close()
    except BaseException as e:
        logger.exception("ИД чата - " + str(p_ChatID) + " - " + str(e))

# Класс текущего состояния по конкретному чату.
# У нас многопользовательский режим, поэтому сохраняем состояние
# каждого чата в списке в своем классе. Потом придется по chat_id
# искать состояние
class ChatClass:
    __slots__ = ['chat_id',
                 'tele_user',
                 'user_id',
                 'fname',
                 'midname',
                 'lastname',
                 'phone',
                 'isadmin',
                 'currentaction',
                 'currentaction2',
                 'currentoperation',
                 'currentoperation2',
                 's_value1',
                 's_value2',
                 's_value3',
                 's_value4',
                 's_value5',
                 'd_value',
                 'i_value',
                 'n_value',
                 ]

    # constructor
    def __init__(self, chartid, teleuser):
        self.chat_id = chartid
        self.tele_user = teleuser
        self.user_id = -1
        self.isadmin = 0
        self.currentaction = 'Questions'
        self.currentoperation = 'ChangeSubj'
        self.currentoperation2 = 'No Action'
        self.s_value1 = ''
        self.s_value2 = ''
        self.s_value3 = ''
        self.s_value4 = ''
        self.s_value5 = ''

    # constructor
    def setphone(self, phone):
        self.phone = phone


# список чатов
AChats = []


def FindChatClass(chat_id):
    ChatInd = 0
    for Chat in AChats:
        if Chat.chat_id == chat_id:
            return ChatInd

        ChatInd = ChatInd + 1

    #Чат не найден, пытаемся считать из БД

    return -1


def SetCurrentChat(chat_id, teleuser, fclear):
    #global db_chat;
    ChatInd = FindChatClass(chat_id)  # Ищем текущий чат по его ИД
    # if chat didn't find then create it
    if ChatInd == -1:
        AChats.append(ChatClass(chat_id, teleuser));
        ChatInd = len(AChats) - 1;
        #db_chat.registerchat(AChats[ChatInd]);
        #AChats[ChatInd].currentoperation = "RegistrUser";
    elif fclear:
        AChats[ChatInd].user_id = -1;
        AChats[ChatInd].currentaction = 'No Action';

    # return the Chat class
    return ChatInd


def sendmesquery(message, txt, repmarkup=None, typemsg=1, imgtext=None):
    # -1 - Значение не принято
    # 1 - запрос данных
    # 2 - Запрос обработан
    # 4 - Для информации
    # иначе - свободное форматирование
    kb = telebot.types.ReplyKeyboardMarkup(True, False);
    kb.row('/start')
    if typemsg == 1:
        text = constants.imPencel + "<i>" + txt + "</i>";
    elif typemsg == 2:
        text = constants.imDone + txt;
    elif typemsg == -1:
        text = constants.imIncorrect + "<i>" + txt + "</i>";
    elif typemsg == 4:
        text = constants.imInfo + txt;
    else:
        if imgtext is not None:
            text = imgtext + txt;
        else:
            text = txt;

    bot.send_message(message.chat.id, text,
                     reply_markup=kb,
                     parse_mode='HTML')

class TKeyboard:
    global AChats;
    #global db_subj;

    def kb_start(self):
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row('/start')
        return kb

    def kb_cancel(self):
        kb = telebot.types.ReplyKeyboardMarkup(True, False)
        kb.row(constants.ButtonCancel);
        return kb;


kb = TKeyboard;

@bot.message_handler(commands=['start'])
def set_welcome(mess):
    global kb;
    global AChats;
    global teleuser;

    kb = TKeyboard();


    # Пользователь телеграм
    teleuser = mess.from_user.username;
    if teleuser is None:
        teleuser = "unknownuser";

    logger.info(msg="Процесс стартовал... " + teleuser);

    if teleuser is None:
        send_image(p_ChatID=mess.chat.id,
                   msgtxt="Необходимо внести изменения в профиль пользователя Telegram и стартовать заново чат командой /start",
                   img_file='teleuserinfo.jpg',
                   bPortal=False,
                   Button=kb.kb_start())
    else:
        # Запоминаем в таблице чатов текущие данные по пользователю
        ChatInd = SetCurrentChat(mess.chat.id, teleuser, True);

        #if AChats[ChatInd].currentoperation == "RegistrUser":
        #    sendmesquery(message=mess,
        #                 txt=constants.welcomeText + "\n" + "Для регистрации требуется согласие на обработку персональных данных",
        #                 repmarkup=kb.#kb_sendcontact(), typemsg=1)
        #else:
        # Приветственное слово
        sendmesquery(message=mess, txt="<b>" + constants.welcomeText + "</b>", typemsg=3);

@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_test(message):
    global kb
    global AChats
    global teleuser

    ChatInd = -1;

    try:
        chat_id = message.chat.id
        ChatInd = FindChatClass(chat_id)

    except:
        pass;

    #возможно была перегрузка системы
    if not ChatInd >= 0:
        set_welcome(message);

    # Текущие переменные окружения
    v = AChats[ChatInd];

    try:
        if message.text == constants.ButtonCancel:
            logger.info("ИД чата - " + str(AChats[ChatInd].chat_id) + " - нажата кнопка " + constants.ButtonCancel[1:100]);
            sendmesquery(message=message,
                         txt="Операция отменена.",
                         typemsg=2)
            v.currentaction = 'Questions'
            v.currentoperation = 'ChangeSubj'
            v.currentoperation2 = ""
            v.s_value1 = ""
            v.s_value2 = ""
            v.s_value3 = ""
            v.s_value4 = ""
        else:
            logger.info("ИД чата - " + str(AChats[ChatInd].chat_id) + " - задан вопрос");
            try:

                reply_markup_mass = {'0': {
                            'reply_markup': {'inline_keyboard': [[
                                {'text':u'\ud83d\udc4d 0','callback_data':'1'},
                                {'text':u'\ud83d\udc4e 0','callback_data':'-1'}
                                                            ]]
                                                            },
                                            'count': {} # [+1, -1]
                                          }
                                }
                #markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
                #itembtn1 = telebot.types.KeyboardButton('a')
                #itembtn2 = telebot.types.KeyboardButton('v')
                #itembtn3 = telebot.types.KeyboardButton('d')
                #markup.add(itembtn1, itembtn2, itembtn3)

                # To Post into a Channel
#                bot.send_message(constants.CHANNEL_NAME, message.text,
#                         parse_mode='HTML',
#                         reply_markup=markup);
                data = {'chat_id': constants.CHANNEL_NAME,
                        'text': message.text,
                        'reply_markup': json.dumps(reply_markup_mass['0']['reply_markup'])}
                requests.get(BOT_URL+'sendMessage',data = data)
                #requests.send_message(constants.CHANNEL_NAME, message.text,
                #         parse_mode='HTML',
                #         reply_markup=markup);
                #Its Ok
                sendmesquery(message=message,
                             txt="Ваш вопрос отправлен.",
                             typemsg=2);
                sendmesquery(message=message,
                             txt="Если необходимо, задайте еще один вопрос:",
                             typemsg=1);
            except BaseException as e:
                logger.exception("ИД чата - " + str(v.chat_id) + " - " + str(e))
                sendmesquery(message=message,
                             txt="произошла ошибка. Повторите ввод:",
                             typemsg=1)


    except BaseException as e:
        sendmesquery(message=message, txt=constants.GErrorText,
                     repmarkup=None, typemsg=-1)
        logger.exception("ИД чата - " + str(v.chat_id) + " - " + str(e))


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def default_photo(message):  # Получить номер телефона
    chat_id = message.chat.id

    try:
        logger.info("ИД чата - " + str(chat_id) + " - Обработка изображений не предусмотрена");
        sendmesquery(message=message, txt="Обработка изображений не предусмотрена. Введите текст!",
                     repmarkup=None, typemsg=-1)
    except BaseException as e:
        sendmesquery(message=message, txt=constants.GErrorText,
                     repmarkup=None, typemsg=-1)
        logger.exception("ИД чата - " + str(chat_id) + " - " + str(e))


@bot.message_handler(func=lambda message: True, content_types=['audio'])
def default_audio(message):  # Получить номер телефона
    chat_id = message.chat.id

    try:
        logger.info("ИД чата - " + str(chat_id) + " - Обработка аудио не предусмотрена");
        sendmesquery(message=message, txt="Обработка аудио не предусмотрена. Введите текст!",
                     repmarkup=None, typemsg=-1)
    except BaseException as e:
        sendmesquery(message=message, txt=constants.GErrorText,
                     repmarkup=None, typemsg=-1)
        logger.exception("ИД чата - " + str(chat_id) + " - " + str(e))


def main():

    try:
        bot.polling(none_stop=True)
    except BaseException as e:
        logger.exception(str(e))
        time.sleep(1)

    while True:
        pass

if __name__ == '__main__':
    
    #app = Flask(__name__)
    main()

