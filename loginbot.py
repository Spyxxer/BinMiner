import telebot
import asyncio, aiohttp
import sys
from urllib import parse
import time
from telebot import types
from telebot import apihelper
from apibot import coins, Login

items = [];


with open("proxies.txt", "r") as file:
	proxies = file.read().split("\n")

proxies.pop()



sys.setrecursionlimit(3000)
TOKEN = "6396911627:AAEVqlJMPqDsf3x26UL8c-P36TzPN-aj6SA"
bot = telebot.TeleBot(TOKEN)
users  = {}; current = None;


async def create_session(id_, csrf, cookie):
	session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), connector_owner=False)

	users[id_]["session"] = session
	msgdict = await Login.check_loginstatus(csrf, cookie, users[id_]["session"])
	#--------------------------------------------------------------------------------#
						#Attempting to authenticate the Login 			
	#---------------------------------------------------------------------------------#
	msgbot = msgdict["message"]
	if msgdict["success"]:
		bot.send_message(id_, msgbot)
		bid = msgdict["userId"]; bnn = msgdict["nickname"]; users[id_]["login"] = True; 
		users[id_]["startTime"] = time.time(); 
		bot.send_message(id_, f"UserId: {bid}\nNickname: {bnn}")
	else:
		bot.send_message(id_, msgbot)



@bot.message_handler(commands=['start'])
def handle_start(message):
	global items
	items = []; text = message.text; chat = message.chat
	id_ = chat.id; 
	users[id_] = {"login":False, "csrf":"", "cookie":"", 
	"session":"", "waitTime":True, "set":set(), "queue":asyncio.Queue()}; 

	#print(users)

	try:
		coins[id_]
	except KeyError:
		coins[id_] = {'boxes':0, 'claimed':0, 'ccoin':"", "tcol":""}

	markup = types.InlineKeyboardMarkup()
	yes = types.InlineKeyboardButton("yes", callback_data='proceed')
	markup.add(yes);
	bot.reply_to(message, "Good day, Are you ready to Login?", reply_markup=markup)


@bot.message_handler(commands=['users'])
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
		coins[id_] = {'boxes':0, 'claimed':0, 'ccoin':"", "tcol":""}

	for key, value in coins[id_].items():
		if key not in ['ccoin', 'tcol', 'boxes', 'claimed']:
			allcoins.append(f"{key} : {value}")
	
	if allcoins:
		allcoins = "\n".join(allcoins)
		bot.reply_to(message, f"[Coins collected]\n________________________________[Last Claimed -> {coins[id_]['ccoin']}]\n[Time: {coins[id_]['tcol']}]\n[Boxes_Found: {coins[id_]['boxes']}]\n[Claims: {coins[id_]['claimed']}]\n_____________________________\n{allcoins}")
	else:
		bot.reply_to(message, f"[Coins collected]\n________________________________")




@bot.message_handler(commands=['decode'])
def handle_cookie(message):
	global current
	text = message.text; chat = message.chat; id_ = chat.id;
	current = bot.send_message(id_, "Enter Cookies to decode the cookies")
	

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
		elif current.text == "Enter Cookies to decode the cookies":
			filtered_cookie = parse.unquote(str(text));
			bot.reply_to(message, filtered_cookie)




@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
	global current, items
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
		#check user identity
		#print("USERID:", users); print() 
		
		#msgApi = await Login.check_loginstatus(users[chat_id]['csrf'], users[chat_id]['cookie'], users[chat_id]['session'])
		bot.answer_callback_query(call.id, f"Attempting Login..Please wait")
		items = [chat_id, users[chat_id]['csrf'].strip(), users[chat_id]['cookie'].strip()]
		




def main():
	try:
		print("Polling..."); 
		bot.polling(non_stop=True)
	except Exception as e:
		print(f"Message: {e}, {sys.exc_info()}, in main polling")
		main()