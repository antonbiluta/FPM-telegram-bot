import os
import telebot
import config
import register
import requests
from tkinter import *
from telebot import types
from db import init_db
from db import add_user
from db import check_reg_user
from db import getName
from db import getSurname
from db import getKurs_Group
from db import getPod_Group
from db import getVk
from db import check_adm
from db import new_adm_db
from db import getPasp
from db import changeRasp
from db import check_day
from db import add_predmet
from db import admin_predmet
from db import getGroupPasp
from db import getAllRasp
from db import getUser

import time
from multiprocessing.context import Process
import schedule


from dbsub import add_subscriber
from dbsub import init_dbsub
from dbsub import update_subscription
from dbsub import check_team
from dbsub import get_subscription
from dbsub import get_subscription_all
from dbsub import get_adm_list
from dbsub import delete_team
from dbsub import add_subscriber_all
from dbsub import delete_user
from db import count_messages
from db import list_messages



bot = telebot.TeleBot(config.TOKEN)
init_db()
group_id = config.GROUP

class User:
    def __init__(self, login):
        self.login=login
        keys = ['chat_id', 'username', 'first_name', 'last_name', 'kurs_group', 'pod_group', 'vk']

        for key in keys:
            self.key = None


def mondey():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='ВТ')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

def tuesday():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='СР')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

def wednesday():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='ЧТ')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

def thursday():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='ПТ')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

def friday():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='СБ')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

def saturday():

    for block in getUser():
        for x in block:
            rasp = getPasp(user_id=x, day='ПН')
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(x, f'Твоё расписание на завтра \n\n{text}')

schedule.every().monday.at("16:00").do(mondey)
schedule.every().tuesday.at("16:00").do(tuesday)
schedule.every().wednesday.at("16:00").do(wednesday)
schedule.every().thursday.at("16:00").do(thursday)
schedule.every().friday.at("16:00").do(friday)
schedule.every().saturday.at("16:00").do(saturday)



class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()



try:
    @bot.message_handler(commands=['start'])
    def welcome(message):
        bot.send_message(message.chat.id, 'Привет, студент! Этот бот создан для того, чтобы ты как можно меньше следил за обновлениями рассписания от деканата.'
                         '\n\nЕсли ты здесь впервые, то пожалуйста, пройти регистрацию по команде /reg'
                         '\n\nНам нужны эти данные, для того, чтобы ты получал правильное рассписание)')

    @bot.message_handler(commands=['test'])
    def test(message):
        pass
    @bot.message_handler(commands=['info'])
    def info(message):
        bot.send_message(group_id, 'hello')

    @bot.message_handler(commands=['reg'])
    def regist(message):
        bot.send_message(message.chat.id, 'Сейчас я проверю, нет ли тебя в базе')
        if (check_reg_user(user_id=message.chat.id)):
            bot.send_message(message.chat.id, 'Такой студент уже числится в базе данных')
            Name = str(getName(user_id=message.chat.id))
            Surname = str(getSurname(user_id=message.chat.id))
            Group = str(getKurs_Group(user_id=message.chat.id))+"/"+str(getPod_Group(user_id=message.chat.id))
            VK = str(getVk(user_id=message.chat.id))
            bot.send_message(message.chat.id, 'Имя: '+Name+'\nФамилия: '+ Surname+'\nГруппа: '+ Group+'\nvk: '+VK +'\n\nЕсли вы не имеете никакого отношения к этим данным - сообщите @antonbiluta')

        else:
            bot.send_message(message.chat.id, 'Все отлично, давай зарегистрируемся!')
            msg = bot.send_message(message.chat.id, 'Введи имя')
            bot.register_next_step_handler(msg, firstname)
    def firstname(message):
        try:
            try:
                User.username = message.from_user.username
            except:
                User.username = message.from_user.first_name
            User.first_name = message.text
            User.chat_id = message.chat.id

            msg = bot.send_message(message.chat.id, 'Введи фамилию')
            bot.register_next_step_handler(msg, lastname)
        except Exception as e:
            bot.reply_to(message, 'ooops!!')
    def lastname(message):
        try:
            User.last_name = message.text

            msg = bot.send_message(message.chat.id, 'Введи номер группы (без подгруппы)')
            bot.register_next_step_handler(msg, kurs_group)

        except Exception as e:
            bot.reply_to(message, 'ooops!!')
    def kurs_group(message):
        try:
            int(message.text)
            User.kurs_group = message.text
            msg = bot.send_message(message.chat.id, 'Введи номер подгруппы')
            bot.register_next_step_handler(msg, pod_group)
        except Exception as e:
            bot.reply_to(message, 'ooops!!')
    def pod_group(message):
        try:
            int(message.text)
            User.pod_group = message.text
            msg = bot.send_message(message.chat.id, 'Дайте ссылку на вк')
            bot.register_next_step_handler(msg, in_vk)
        except Exception as e:
            bot.reply_to(message, 'ooops!!')
    def in_vk(message):
        try:
            User.vk = message.text
            msg = bot.send_message(User.chat_id, 'Данные будут отправлены на обработку!'
                                            '\nОжидайте ответа')
            bot.register_next_step_handler(msg, reg_finish('Ok'))
        except Exception as e:
            bot.reply_to(message, 'ooops!!')
    def reg_finish(message):
        markup = types.InlineKeyboardMarkup()
        ok_btn = types.InlineKeyboardButton('Одобрить', callback_data=1)
        no_btn = types.InlineKeyboardButton('Заброковать', callback_data=2)
        markup.add(ok_btn, no_btn)

        bot.send_message(group_id, 'id: '+str(User.chat_id)+
                                   '\nИмя: '+User.first_name+
                                   '\nФамилия: '+User.last_name+
                                   '\nГруппа: '+User.kurs_group+
                                   '\nПодгруппа: '+User.pod_group+
                                   '\nVK: '+User.vk, reply_markup=markup)


    @bot.message_handler(commands=['getstar'])
    def getstar(message):
        if check_reg_user(user_id=message.chat.id):
            if check_adm(user_id=message.chat.id):
                bot.send_message(message.chat.id, 'У вас уже есть "Староста".'
                                                  '\nЕсли возник вопрос, напишите @antonbiluta')
            else:
                global star_id
                global star_name
                try:
                    star_name = message.from_user.username
                except:
                    star_name = message.from_user.first_name
                star_id = message.chat.id
                bot.send_message(message.chat.id, 'Твоя заявка была отправлена на рассмотрение')
                markup = types.InlineKeyboardMarkup()
                star_btn = types.InlineKeyboardButton('Староста', callback_data='Starosta_ok')
                zstar_btn = types.InlineKeyboardButton('Зам', callback_data='Zamstarosta_ok')
                starno_btn = types.InlineKeyboardButton('Отклонить', callback_data='Starosta_no')
                markup.add(star_btn, zstar_btn, starno_btn)

                bot.send_message(group_id, 'Заявка на старосту'
                                 '\nid: ' + str(star_id) +
                                 '\nИмя: ' + str(getName(user_id=star_id)) +
                                 '\nФамилия: ' + str(getSurname(user_id=star_id)) +
                                 '\nГруппа: ' + str(getKurs_Group(user_id=star_id)) + '/' + str(getPod_Group(user_id=star_id)) +
                                 '\nVK: ' + str(getVk(user_id=star_id)), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста зарегистрируйтесь по команде /reg .')

    @bot.message_handler(commands=['help'])
    def help(message):
        if(check_adm(user_id=message.chat.id)):
            bot.send_message(message.chat.id, 'Ты у нас с правами, поэтому получай особую помощь.')
            bot.send_message(message.chat.id, 'В твоём распоряжении админ меню'
                                              '\nПожалуйста, не балуйся, иначе @antonbiluta тебя снимет))'
                                              '\n\nВашему вниманию предлагаются такие команды как:'
                                              '\n/admin'
                                              '\n/changeday - поменять аудиторию в один из дней на опр пару'
                                              '\n/dayadd - добавить пары на определенный день'
                                              '\n\nЕсли тебе вдруг надоело быть с привелегией, сообщи мне('
                                              '\nТак же помни, что команды каждый раз пополняются, поэтому не забывай время от '
                                              'времени проверять данное руководство')

        else:
            bot.send_message(message.chat.id, 'Этот бот создан программистом для программистов :)'
                                              '\nЕсли вы устали проверять деканат на обновления расписания, то забудьте! '
                                              'Теперь этим страдает администрация бота'
                                              '\n\nВашему вниманию предлагаются такие команды как:'
                                              '\n/start'
                                              '\n/help'
                                              '\n/getstar - чтобы запросить себе звание "Староста" или "Зам.Староста"'
                                              '\n/rgadmin - чтобы запросить себе админку или редактора'
                                              '\n\nЕсли вас интересует расприсание на понедельник, введите в чат: ПН'
                                              '\nЕсли у вас в понедельник есть пары, которые деляться на числ/знам, то писать нужно ПН/1 - числ, ПН/2 - знам.'
                                              '\nХочу пары на числитель - СР/1'
                                              '\nНадеюсь, студент, ты меня хорошо понял)')

    @bot.message_handler(commands=['rgadmin'])
    def rgadm(message):
        if check_reg_user(user_id=message.chat.id):
            if check_adm(user_id=message.chat.id):
                bot.send_message(message.chat.id, 'У вас уже имеются права.'
                                                  '\nЕсли вы хотите повышения, напишите @antonbiluta')
            else:
                global adm_id
                global adm_name
                try:
                    adm_name = message.from_user.username
                except:
                    adm_name = message.from_user.first_name
                adm_id = message.chat.id
                bot.send_message(message.chat.id, 'Твоя заявка была отправлена на рассмотрение')
                markup = types.InlineKeyboardMarkup()
                admin_btn = types.InlineKeyboardButton('Админка', callback_data='admin_ok')
                red_btn = types.InlineKeyboardButton('Редактор', callback_data='redactor_ok')
                bad_btn = types.InlineKeyboardButton('Отклонить', callback_data='admin_no')
                markup.add(admin_btn, red_btn, bad_btn)

                bot.send_message(group_id, 'Заявка на администратора'
                                 '\nid: ' + str(adm_id) +
                                 '\nИмя: ' + str(getName(user_id=adm_id)) +
                                 '\nФамилия: ' + str(getSurname(user_id=adm_id)) +
                                 '\nГруппа: ' + str(getKurs_Group(user_id=adm_id)) + '/' + str(getPod_Group(user_id=adm_id)) +
                                 '\nVK: ' + str(getVk(user_id=adm_id)), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста зарегистрируйтесь по команде /reg .')

    #Админка
    @bot.message_handler(commands=['admin'])
    def admin(message):
        if(check_adm(user_id=message.chat.id)):
            msg = bot.send_message(message.chat.id, 'Вы успешно подключились к админ панели!')
            bot.register_next_step_handler(msg, choose_command)
        else:
            bot.send_message(message.chat.id, 'У вас не достаточно прав для использования этой команды.')
    def choose_command(message):
        bot.send_message(message.chat.id, 'Разработка')

    @bot.message_handler(commands=['changeday'])
    def changeday(message):
        if(check_adm(user_id=message.chat.id)):
            bot.send_message(message.chat.id, 'Ты можешь изменить только расписание своей группы')
            msg = bot.send_message(message.chat.id, 'Введи подгруппу, где хочешь сделать изменения: 1, 2 ')
            bot.register_next_step_handler(msg, find_group)
        else:
            bot.send_message(message.chat.id, 'Сделайте запрос на администратора')
    def find_group(message):
        global pod_group
        pod_group = message.text
        msg = bot.send_message(message.chat.id,
                         'Введи день, где хочешь сделать изменения: ПН/1, ПН/2, ПН(только для дней, где нет деления на числитель/знаменатель)')
        bot.register_next_step_handler(msg, find_day)
    def find_day(message):
        global day
        day = message.text
        msg = bot.send_message(message.chat.id, 'Какую по счёту пару надо поменять? 1-8')
        bot.register_next_step_handler(msg, find_num)
    def find_num(message):
        global num
        num = message.text
        msg = bot.send_message(message.chat.id, 'Введи новую аудиторию')
        bot.register_next_step_handler(msg, find_audit)
    def find_audit(message):
        audit = message.text
        changeRasp(user_id=message.chat.id, pod_group=pod_group, day=str(day), num=num, audit=str(audit))

        rasp = check_day(user_id=message.chat.id, pod_group=pod_group, day=day)
        text = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)}:  {str(message_text)}. Аудитория: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])
        bot.send_message(message.chat.id, 'Расписание на ' + day + ' для вашей группы ' + pod_group + ' подгруппы:'
                                                                                                      '\n\n' + str(text))

    @bot.message_handler(commands=['dayadd'])
    def dayadd(message):
        if (check_adm(user_id=message.chat.id)):
            global chat_id_temp
            chat_id_temp = message.chat.id
            bot.send_message(message.chat.id, 'Ты в режиме добавления нового предмета.\nВажно, добавить ты можешь 1 предмет '
                                              'за 1 раз.\n\nДобавляй по очереди, как идут. Иначе будешь получать пары как 3,4,1,2 а не 1,2,3,4')
            msg = bot.send_message(message.chat.id, 'Укажи подгруппу: 1/2')
            bot.register_next_step_handler(msg, set_group)
        else:
            bot.send_message(message.chat.id, 'Сделайте запрос на администратора')
    def set_group(message):
        global pod_group
        pod_group = message.text
        msg = bot.send_message(message.chat.id, 'Укажи день: ПН/1 ПН/2 или ПН (если нет пар с разделением на числитель/знаменатель)')
        bot.register_next_step_handler(msg, set_day)
    def set_day(message):
        global day
        day = message.text
        msg = bot.send_message(message.chat.id, 'Укажите номер пары и все её данные')
        bot.register_next_step_handler(msg, set_num)
    def set_num(message):
        if message.text == 'stop':
            bot.send_message(chat_id_temp, 'Все данные сохранены')
            rasp = getPasp(user_id=chat_id_temp, day=day)
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)}:  {str(message_text)}. Аудитория: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(message.chat.id, 'Расписание на ' + str(day) + '\n\n' + str(text))

        else:
            global num
            global timeline
            num = message.text
            if message.text == '1':
                timeline = '8:00-9:30'
            elif message.text == '2':
                timeline = '9:40-11:10'
            elif message.text == '3':
                timeline = '11:30-13:00'
            elif message.text == '4':
                timeline = '13:10-14:40'
            elif message.text == '5':
                timeline = '15:00-16:30'
            elif message.text == '6':
                timeline = '16:40-18:10'
            elif message.text == '7':
                timeline = '18:30-??:??'
            elif message.text == '8':
                timeline = '??:??-??:??'
            msg = bot.send_message(message.chat.id, 'Напишите предмет. К примеру: Мат.Анализ II (Сеидова)')
            bot.register_next_step_handler(msg, set_predmet)
    def set_predmet(message):
        global predmet
        predmet = message.text
        msg = bot.send_message(message.chat.id, 'Введите аудиторию. К примеру: А301б или 115 ауд. ИНСПО')
        bot.register_next_step_handler(msg, set_audit)
    def set_audit(message):
        audit = message.text
        add_predmet(user_id=chat_id_temp, pod_group=pod_group, day=day, num=num, predmet=predmet, audit=audit, timeline=timeline)
        msg = bot.send_message(message.chat.id, 'Вы можете написать stop или продолжить записывать пары.')
        bot.register_next_step_handler(msg, set_num)

    @bot.message_handler(commands=['get'])
    def get(message):
        if(check_reg_user(user_id=message.chat.id)):
            msg = bot.send_message(message.chat.id, 'Введите группу')
            bot.register_next_step_handler(msg, getgroup)
        else:
            bot.send_message(message.chat.id, 'Зарегайся, чорт')
    def getgroup(message):
        global group
        group = message.text
        msg = bot.send_message(message.chat.id, 'Введите подгруппу')
        bot.register_next_step_handler(msg, getpodgroup)
    def getpodgroup(message):
        global pod_group
        pod_group = message.text
        msg = bot.send_message(message.chat.id, 'Введите день: ПН, ПН/1, ПН/2')
        bot.register_next_step_handler(msg, getday)
    def getday(message):
        day = message.text

        rasp = getAllRasp(group=group, pod_group=pod_group, day=day)
        text = '\n'.join([f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for message_Num, message_timeline, message_text, message_audit in rasp])

        bot.send_message(message.chat.id, f'Расписание {str(group)}/{str(pod_group)} на {str(day)}:\n\n{str(text)}')


    @bot.message_handler(commands=['getall'])
    def getall(message):
        if (check_reg_user(user_id=message.chat.id)):
            msg = bot.send_message(message.chat.id, 'Введите группу')
            bot.register_next_step_handler(msg, getgroupall)
        else:
            bot.send_message(message.chat.id, 'Зарегайся, чорт')
    def getgroupall(message):
        global group
        group = message.text
        msg = bot.send_message(message.chat.id, 'Введите подгруппу')
        bot.register_next_step_handler(msg, getpodgroupall)
    def getpodgroupall(message):
        pod_group = message.text
        rasp = getAllRasp(group=group, pod_group=pod_group, day='ПН')
        pn = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])
        rasp = getAllRasp(group=group, pod_group=pod_group, day='ВТ')
        vt = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])

        rasp = getAllRasp(group=group, pod_group=pod_group, day='СР')
        sr = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])

        rasp = getAllRasp(group=group, pod_group=pod_group, day='ЧТ')
        cht = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])

        rasp = getAllRasp(group=group, pod_group=pod_group, day='ПТ')
        pt = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])

        rasp = getAllRasp(group=group, pod_group=pod_group, day='СБ')
        sb = '\n'.join(
            [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}' for
             message_Num, message_timeline, message_text, message_audit in rasp])

        bot.send_message(message.chat.id, f'Расписание {str(group)}/{str(pod_group)}:\n\n{str(pn)}\n\n{str(vt)}\n\n{str(sr)}')


    @bot.message_handler(commands=['addgroup'])
    def dayadd(message):
        if (check_adm(user_id=message.chat.id)):
            bot.send_message(message.chat.id, 'Ты в режиме добавления нового предмета.\nВажно, добавить ты можешь 1 предмет '
                                              'за 1 раз.\n\nДобавляй по очереди, как идут. Иначе будешь получать пары как 3,4,1,2 а не 1,2,3,4')
            msg = bot.send_message(message.chat.id, 'Укажи номер группы')
            bot.register_next_step_handler(msg, set_main)
        else:
            bot.send_message(message.chat.id, 'Сделайте запрос на администратора')
    def set_main(message):
        global group_main
        group_main = message.text
        msg = bot.send_message(message.chat.id,
                               'Укажи подгруппу: 1/2')
        bot.register_next_step_handler(msg, set_group_1)
    def set_group_1(message):
        global pod_group
        pod_group = message.text
        msg = bot.send_message(message.chat.id, 'Укажи день: ПН/1 ПН/2 или ПН (если нет пар с разделением на числитель/знаменатель)')
        bot.register_next_step_handler(msg, set_day_1)
    def set_day_1(message):
        global day
        day = message.text
        msg = bot.send_message(message.chat.id, 'Укажите номер пары и все её данные')
        bot.register_next_step_handler(msg, set_num_1)
    def set_num_1(message):
        if message.text == 'stop':
            bot.send_message(message.chat.id, 'Все данные сохранены')
            rasp = getGroupPasp(group=group_main, podgroup=pod_group, day=day)
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)}:  {str(message_text)}. Аудитория: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(message.chat.id, 'Расписание '+str(group_main)+'/'+str(pod_group)+' на '+ str(day) + '\n\n' + str(text))

        else:
            global num
            global timeline
            num = message.text
            if message.text == '1':
                timeline = '8:00-9:30'
            elif message.text == '2':
                timeline = '9:40-11:10'
            elif message.text == '3':
                timeline = '11:30-13:00'
            elif message.text == '4':
                timeline = '13:10-14:40'
            elif message.text == '5':
                timeline = '15:00-16:30'
            elif message.text == '6':
                timeline = '16:40-18:10'
            elif message.text == '7':
                timeline = '18:30-??:??'
            elif message.text == '8':
                timeline = '??:??-??:??'
            msg = bot.send_message(message.chat.id, 'Напишите предмет. К примеру: Мат.Анализ II (Сеидова)')
            bot.register_next_step_handler(msg, set_predmet_1)
    def set_predmet_1(message):
        global predmet
        predmet = message.text
        msg = bot.send_message(message.chat.id, 'Введите аудиторию. К примеру: А301б или 115 ауд. ИНСПО')
        bot.register_next_step_handler(msg, set_audit_1)
    def set_audit_1(message):
        audit = message.text
        admin_predmet(group=group_main, pod_group=pod_group, day=day, num=num, predmet=predmet, audit=audit, timeline=timeline)
        msg = bot.send_message(message.chat.id, 'Вы можете написать stop или продолжить записывать пары.')
        bot.register_next_step_handler(msg, set_num_1)

    @bot.message_handler(content_types=['text'])
    def any(message):
        if(check_reg_user(user_id=message.chat.id)):
            rasp = getPasp(user_id=message.chat.id, day=message.text)
            text = '\n'.join(
                [f'{str(message_Num)}. {str(message_timeline)}:  {str(message_text)}. Аудитория: {str(message_audit)}' for
                 message_Num, message_timeline, message_text, message_audit in rasp])
            bot.send_message(message.chat.id, 'Расписание на ' + message.text + '\n\n' + str(text))
        else:
            bot.send_message(message.chat.id, 'Используй /reg')


    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == '1':
            bot.send_message(call.message.chat.id, 'Заявка была одобрена!')
            bot.answer_callback_query(callback_query_id=call.id, text='Заявка одобрена!')
            bot.send_message(User.chat_id, 'Ваша заявка была одобрена администрацией!')
            add_user(
                user_id=User.chat_id,
                username=str(User.username),
                first_name=User.first_name,
                last_name=User.last_name,
                kgroup=User.kurs_group,
                podgroup=User.pod_group,
                vk=User.vk
            )
        elif call.data == '2':

            bot.send_message(call.message.chat.id, 'Заявка была отклонена =(')
            bot.answer_callback_query(callback_query_id=call.id, text='Заявка отклонена =(')
            bot.send_message(User.chat_id, 'Ваша заявка была отклонена администрацией =(')
            bot.send_message(User.chat_id, 'Возможно в данных была допущена ошибка по мнению администрации'
                                      '\nПожалуйста перепройдите /reg указывая настоящие данные'
                                      '\n\nИли свяжитесь с @antonbiluta, чтобы узнать подробности.')
        elif call.data == 'admin_ok':

            bot.send_message(call.message.chat.id, 'Пользователь стал администратором!')
            bot.answer_callback_query(callback_query_id=call.id, text='Новый админ!"')
            bot.send_message(adm_id, 'Вы стали администратором! Для подробностей о всех ваших возможностях, введите /help - '
                                     'там тебя ждут совсем другие инструкции)')
            new_adm_db(
                user_id=adm_id,
                username=adm_name,
                perm='Администратор'
            )
        elif call.data == 'redactor_ok':

            bot.send_message(call.message.chat.id, 'Пользователь стал редактором!')
            bot.answer_callback_query(callback_query_id=call.id, text='Новый редактор!')
            bot.send_message(adm_id, 'Вы стали редактором!Для подробностей о всех ваших возможностях, введите /help - '
                                     'там тебя ждут совсем другие инструкции)')
            new_adm_db(
                user_id=adm_id,
                username=adm_name,
                perm='Редактор'
            )
            bot.send_message(adm_id, 'Для подробностей о всех ваших возможностях, введите /help - '
                                     'там тебя ждут совсем другие инструкции)')
        elif call.data == 'admin_no':

            bot.send_message(call.message.chat.id, 'Заявка на пермишн была отклонена.')
            bot.answer_callback_query(callback_query_id=call.id, text='Заявка отклонена =(')
            bot.send_message(adm_id, 'Ваш запрос на пермишн получил отказ.')
        elif call.data == 'Starosta_ok':
            bot.send_message(call.message.chat.id, 'Пользователь стал старостой!')
            bot.answer_callback_query(callback_query_id=call.id, text='Новый админ!"')
            bot.send_message(star_id, 'Вы получили "Старосту"!')
            new_adm_db(
                user_id=star_id,
                username=star_name,
                perm='Староста'
            )
        elif call.data == 'Zamstarosta_ok':
            bot.send_message(call.message.chat.id, 'Пользователь стал зам старосты!')
            bot.answer_callback_query(callback_query_id=call.id, text='Новый зам!"')
            bot.send_message(star_id, 'Вы получили "Зам.Старосты"!')
            new_adm_db(
                user_id=star_id,
                username=star_name,
                perm='Зам.Старосты'
            )
        elif call.data == 'Starosta_no':
            bot.send_message(call.message.chat.id, 'Заявка на старосту была отклонена.')
            bot.answer_callback_query(callback_query_id=call.id, text='Заявка отклонена =(')
            bot.send_message(star_id, 'Ваш запрос на старосту получил отказ.')


        #bot.edit_message_reply_markup(group_id, call.message.message_id)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def command_default(message):
        str(message.text)
        if message.chat.type == 'private':

            if message.text == '🕰Команда Прошлого🕰':


                if check_team(user_id=message.chat.id, team='Прошлое') is True:
                    bot.send_message(message.chat.id, 'Ты уже есть в команде Прошлого!')

                elif check_team(user_id=message.chat.id, team='Будущее') is True:
                    bot.send_message(message.chat.id, 'Ты уже есть в другой команде!'
                                                      '\nЕсли хочешь сменить, пропиши /start и повтори свой выбор.')

                elif check_team(user_id=message.chat.id, team='Общая') is True:
                    update_subscription(user_id=message.chat.id, team='Прошлое')

                    bot.send_message(message.chat.id,
                                     'Привет, команда прошлого ❤'
                                     '\nМы подготовили для тебя несколько интересных заданий на разных площадках города, '
                                     'но сможешь ли ты с ними справится?😏 '
                                     '\nЕсли вдруг ты ошибся командой, пропиши /start.')

            elif message.text == '🧬Команда Будущего🧬':

                if check_team(user_id=message.chat.id, team='Будущее') is True:
                    bot.send_message(message.chat.id, 'Ты уже есть в команде Будущего!')

                elif check_team(user_id=message.chat.id, team='Прошлое') is True:
                    bot.send_message(message.chat.id, 'Ты уже есть в другой команде!'
                                                      '\nЕсли хочешь сменить, пропиши /start и повтори свой выбор.')

                elif check_team(user_id=message.chat.id, team='Общая') is True:
                    update_subscription(user_id=message.chat.id, team='Будущее')
                    bot.send_message(message.chat.id,
                                     'Привет, команда будущего ❤'
                                     '\nМы подготовили для тебя несколько интересных заданий на разных площадках города, '
                                     'но сможешь ли ты с ними справится?😏 '
                                     '\nЕсли вдруг ты ошибся командой, пропиши /start.')

except:
    @bot.message_handler(content_types=['text'])
    def error(message):
        bot.send_message(group_id, 'Вызвана ошибка')


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
