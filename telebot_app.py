# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 00:43:19 2020

@author: krishna chaitanya
"""


from covid_study import gettotaldata,getstatesdata
import time
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

token="1275885484:AAH_GK3b57Ak2RfGnXP6v8V9cXHku4km52M"
bot = telebot.TeleBot(token)
user = bot.get_me()
scheduler=BackgroundScheduler()
scheduler.start()

help="""
Welcome to IARE COVID-19 Bot

/start : to start converstion
/statename@data : to get data of that state 

NOTE : Telangana is spelled as Telengana in mohfw.gov.in

e.g : /Telengana@data 

/total_cases : India Statistics
/update@freq : For automated updates daily

e.g :
/update@1D : Update only ONCE Per DAY

/update@12H : update every 12Hours

/update@5M : update every 5Min

/update@10S : update every 10Sec

/stop : For stop receiving updates
"""
print(help)
freq=(0,0)#freq,day
day=0


def make_freq(updt):
    i_freq=updt.split('@')[1]
    if 'H' in i_freq:
        return (int(i_freq.replace('H','').strip() or 0)*3600,0)
    if 'M' in i_freq:
        return (int(i_freq.replace('M','').strip() or 0)*60,0)
    if 'S' in i_freq:
        return (int(i_freq.replace('S','').strip() or 0),0)
    if 'D' in i_freq:
        return (0,int(i_freq.replace('D','').strip() or 0))
    else:
        return (0,0)
        
        
def state_name(msg):
    if '@' in str(msg) and msg.split('@')[1]=='data':
        return msg.split('@')[0].replace('/','')
    else:
        return 'Wrong Input\n'+help
        
@bot.message_handler(commands=['start','help'])
def send_welcome(message):
	bot.reply_to(message, help)

@bot.message_handler(commands=['total_cases'])
def send_totalcases(message):
    bot.reply_to(message,gettotaldata())

@bot.message_handler(commands=['stop'])
def stop_updates(message):
    if(scheduler.get_job(str(message.from_user.id)) is not None):
        scheduler.remove_job(str(message.from_user.id))
        bot.reply_to(message,'job removed ')
    else:
        bot.reply_to(message,'No Subscirption')

@bot.message_handler(func=lambda msg : msg.text is not None and '@' in msg.text and 'update' not in msg.text)
def send_statedata(message):
    rep=state_name(message.text)
    if 'Wrong Input' not in rep:
        bot.reply_to(message,getstatesdata(rep))
    else:
        bot.reply_to(message,rep)



@bot.message_handler(func=lambda msg : msg.text is not None and '@' in msg.text and 'update' in msg.text)
def send_daily(message):
    global freq
    freq=make_freq(message.text)
    bot.reply_to(message,'Send me the state name!')

@bot.message_handler(func=lambda msg : msg.text is not None and '@' not in msg.text)
def send_daily_state(message):
    global freq
    state=message.text
    chat_id=message.chat.id
    first_nm=message.from_user.first_name
    last_nm=message.from_user.last_name
    bot.send_message(chat_id,str(freq))
    if freq[0]>0 and freq[1]==0 and state!='':
        scheduler.add_job(send_updates, 'interval',[chat_id,state,first_nm,last_nm],seconds=freq[0],id=str(message.from_user.id),replace_existing=True)
    elif freq[1]>0 and freq[0]==0 and state!='':
        scheduler.add_job(send_updates,'interval',[chat_id,state,first_nm,last_nm],days=freq[1],id=str(message.from_user.id),replace_existing=True)
    
def generate_update(state,first_nm,last_nm):
    return ('Hi '+str(first_nm)+' '+str(last_nm)+'\n'+'The update is here : \n'+getstatesdata(state))
    
def send_updates(chat_id,state,first_nm,last_nm):
        bot.send_message(chat_id,generate_update(state,first_nm,last_nm))



#if freq[0]>0 and freq[1]==0 and state!='':
    #scheduler.add_job(send_updates, 'interval', seconds=freq[0],id='implicit',replace_existing=True)
    


while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
