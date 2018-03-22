# -*- coding: utf-8 -*-
#CHANNEL_NAME = '-1001351153971' #канал вопросов
CHANNEL_NAME = '@test_chanckbi'
CHANNEL_NAME_ADM = '-1001315761021'
#TOKEN = app.config['TOKEN']
#WEBHOOKURL = app.config['WEBHOOKURL']
#BOT_URL = 'https://api.telegram.org/bot'

noteleuser = "Для работы с ботом ЦК BI <b>заведите</b> в своем профиле telegramm <b>username</b> для дальнейшей идентификации!\nДалее нажмите на кнопку <b>/start</b>."

dir_image = 'img/'

log00010 = "Вошел в систему"
log00011 = "Вышел из системы"
log00020 = "Попытка регистрации в системе"

imWelcome   = u'\U0001F418'

imNews      = u'\U0001F4C3';
imHBD       = u'\U0001F385';
imRecl      = u'\U0001F4EE';
imMyState   = u'\U0001F430';
imProjInfo  = u'\U0001F4DD';
imAdmin     = u'\U0001F511';
imCKBI      = u'\U0001F3E0';
imCancel    = u'\U00002734';
imDone      = u'\U00002714';
imIncorrect = u'\U0000203C';
imOk        = u'\U00002705';
imNo        = u'\U0000274C';
imInfo      = u'\U0000261D';
imInfoCK    = u'\U0001F4D6';
imPencel    = u'\U0000270F';
imRegistr   = u'\U0001F511';
imBotAnswer = u'\U00002714';
imFace      = u'\U0001F5FF';
imBell      = u'\U0001F514';
imPhone     = u'\U0000260E';
imQuestion  = u'\U00002049';
imVote      = u'\U00002611';

ButtonMeeting           = imNews + 'Задать вопрос'
ButtonHBD               = imHBD + 'Что впереди'
ButtonRecl              = imRecl + 'Отправить Feedback разработчикам'
ButtonMyState           = imMyState + 'Мой статус'
ButtonProjInfo          = imProjInfo + 'Проект-инфо'
ButtonAdmin             = imAdmin + 'Администрирование'
ButtonCKBI              = imCKBI + 'ЦК BI'
ButtonReclSimple        = imRecl + 'Простая форма'
ButtonRegist            = imRegistr + 'Регистрация'
ButtonAgreeContactInf   = imOk + 'Согласен на обработку и регистрацию'
ButtonCKBIZoneAC        = imInfoCK + 'Информация по АС'
ButtonCKBIVect          = imInfoCK + 'Ответственность по направлениям'
ButtonGetLogFile        = 'Получить LOG'
ButtonAdminInfo         = imAdmin+'Координаты администратора'
ButtonQuestion         = imBell+'Текущие опросы'
ButtonAdminCntUsers     = 'Количество пользователей'
ButtonMetadata          = imInfo+'Запрос метаданных'
ButtonTS                = imPhone + 'Тел. справочник'
ButtonQuestions         = imQuestion + 'Задать вопрос'
ButtonVote              = imVote     + 'Проголосовать'

ButtonCancel         = imCancel + 'Отмена'
ButtonYes            = imOk + 'Да'
ButtonNo             = imNo + 'Нет'
ButtonNextMetadata   = imInfo + 'Еще'

welcomeText     =  "Добро пожаловать в наш Бот!\nЗдесь Вы можете:\n   1. Задать вопрос руководству в канал вопросов Департамента фабрики данных (https://t.me/ckmeet_questions)\n   2. Осуществить обратную связь с разработчиками по вопросам работы бота и каналов"
GErrorText      =  'Вах-вах-вах... Произошла непредвиденная ошибка.\nПовторите операцию или попробуйте что-то еще.\n' \
                   'Нам не безразличны Ваши проблемы!\nМы ими займемся в ближайшее время...'

restartText     = '\n'

sql_save_user = """Insert into tUsers (chat_id,tele_user, isadmin, currentaction, currentoperation) value(%s,'%s', 0, '%s', '%s') on duplicate key update currentaction='%s',currentoperation='%s';"""
sql_save_question = """insert into tQuestions(chat_id, subjmeet_id, ques_descr) values (%s, %s, '%s');"""