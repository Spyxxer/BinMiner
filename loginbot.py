import telebot
import asyncio
import sys
import time
from telebot import types
from telebot import apihelper
from apibot import Login, coins

sys.setrecursionlimit(3000)
TOKEN = "5212303360:AAGa9JGEJTtTpLwk2mMdoVtWPpIpOZcCiWQ"
bot = telebot.TeleBot(TOKEN)
i = 0
users  = {}
current = None;


@bot.message_handler(commands=['start'])
def handle_start(message):
	text = message.text; chat = message.chat
	id_ = chat.id; users[id_] = {"login":False, "startTime":0, "csrf":"", "cookie":"", 
	"session":Login.session, "waitTime":False}; 

	try:
		coins[id_]
	except KeyError:
		coins[id_] = {}

	markup = types.InlineKeyboardMarkup()
	yes = types.InlineKeyboardButton("yes", callback_data='proceed')
	markup.add(yes);
	bot.reply_to(message, "Good day, Are you ready to Login?", reply_markup=markup)


@bot.message_handler(commands=['currentusers'])
def handle_users(message):
	usersarr = []
	for key, value in users.items():
		usersarr.append(f"USER_ID : {key}\nLogin Status : {users[key]['login']}")
	currentusers_ = "\n\n".join(usersarr)
	if usersarr:
		bot.reply_to(message, f"[Current Users]\n____________________________\n{currentusers_}")
	else:
		bot.reply_to(message, "Current Users: None")

@bot.message_handler(commands=['coins'])
def handle_coins(message):
	allcoins = []; id_ = message.chat.id
	
	try:
		coins[id_]
	except KeyError:
		coins[id_] = {}

	for key, value in coins[id_].items():
		allcoins.append(f"{key} : {value}")
	
	if allcoins:
		allcoins = "\n".join(allcoins)
		bot.reply_to(message, f"[Coins collected]\n________________________________\n{allcoins}")
	else:
		bot.reply_to(message, f"[Coins collected]\n________________________________")


@bot.message_handler(func=lambda message:True)
def handle_message(message):
	text = message.text; video = message.video
	if video:
		bot.reply_to(message, "This is a video")
	else:
		if current.text == "Enter CSRF_TOKEN":
			markup = types.InlineKeyboardMarkup()
			yes = types.InlineKeyboardButton("yes", callback_data="proceed_cookies")
			no = types.InlineKeyboardButton('no', callback_data="proceed")
			markup.row(yes, no); bot.reply_to(message, f"CSRF_TOKEN:{text}\n\nIs this correct?", reply_markup=markup)
		elif current.text == "Enter Cookies":
			markup = types.InlineKeyboardMarkup()
			yes = types.InlineKeyboardButton("yes", callback_data="done")
			no = types.InlineKeyboardButton('no', callback_data="proceed_cookies")
			markup.row(yes, no); bot.reply_to(message, f"Cookies:{text}\n\nIs this correct?", reply_markup=markup)




@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
	global current
	chat = call.from_user; chat_id = chat.id; name = chat.first_name	
	if call.data == "proceed":
		bot.answer_callback_query(call.id, 'Ok')
		bot.send_message(chat_id, f"id:{chat_id}, name:{name}")
		bot.send_message(chat_id, "CSRF_TOKEN and Cookies can be gotten from Request header after successful login")
		current = bot.send_message(chat_id, "Enter CSRF_TOKEN")		
	elif call.data == "proceed_cookies":
		bot.answer_callback_query(call.id, 'CSRF_TOKEN Accepted.')
		csrf = call.message.reply_to_message.text
		users[chat_id]["csrf"] = csrf;
		current = bot.send_message(chat_id, "Enter Cookies")
	elif call.data == "done":
		cookie = call.message.reply_to_message.text
		bot.answer_callback_query(call.id, 'Cookies Accepted.')
		users[chat_id]["cookie"] = cookie;
		print("USERID:", users); print() 
		msgApi = Login.check_loginstatus(users[chat_id]['csrf'], users[chat_id]['cookie'], users[chat_id]['session'])
		msgdict = msgApi 
		msgbot = msgdict["message"];
		
		bot.answer_callback_query(call.id, f"Attempting Login..Please wait")
		if msgdict["success"]:
			bot.send_message(chat_id, msgbot)
			bid = msgdict["userId"]; bnn = msgdict["nickname"]; users[chat_id]["login"] = True; 
			users[chat_id]["startTime"] = time.time(); 
			bot.send_message(chat_id, f"UserId:{bid}\nNickname:{bnn}")
		else:
			bot.send_message(chat_id, msgbot)


def main():
	try:
		print("Polling..."); bot.polling(non_stop=True)
	except Exception as e:
		print(f"Message: {e}, {sys.exc_info()}, in main polling")
		main()