from telethon.sync import TelegramClient, events
from telethon.tl import functions, types
from getpass import getpass
from telethon.errors import *
import asyncio, sys, re, time, traceback, datetime, os
import aiofiles, logging, aiohttp
from PIL import Image
from colorama import Fore, Style, init
from inspect import signature, Parameter
from collections import deque
import enchant, aiohttp
import loginbot, threading


init()

logging.basicConfig(filename='TGLOG.log', level=logging.DEBUG)
#These can be gotten from my.telegram.org/auth
api_id = '22136951' #Your api_id Spxxer account
api_hash = 'cd0b7f1a9f8d02328257366cd76bc8ba' #Your api_hash

api_id2 = '23762301' #DO account
api_hash2 = '9fd996011546868d890ed7b5cc9975ee'


#download_picture_path = str(input("Insert download_pic Path:"))


class Paste:
	def __init__(self):
		self.run = True; self.k = ''; self.rot = 0
		self.open = 0; self.claim = 0; self.today = str(datetime.date.today())
		self.asyc_q = asyncio.Queue();
		self.boxarr = {0:["safe_crypto_box", -1001819819794], 3:["My_Channel", -1002092644299],
		29:["abemav", -1001569554310],
		2:["Box_Tiger", -1001865918932], 5:["sheikhbd1box", -1001838514169], 
		1:["cryptolily", -1001879285492], 4:["freebinancebox1", -1001771475697], 
		6:["Binance Box", -1001903795294], 7:["CRYPTO_FREEX", -1001930686672], 
		8:["Kalina_Chats", -1001605383733], 10:["XCOINBOXES", -1001748979180], 
		11:["CryptoBoxLive", -1001766025385],12:["hit_crypto_world", -1001865925714], 
		14:["Crypto_Box_forever", -1001702563167], 15:["King_BOX", -1001514969433],
		16:["Russellcoin", -1001903905245], 17:["Crypto_Box_Codes", -1001966861515],
		18:["Bnncbox", -1001767498343], 19:["Crypto_Tree", -1001598899681],
		20:["Early_Rivo", -1001947934413], 21:["MDN_BOX", -1001956148602],
		22:["Binance solve", -1001907810866], 23:["Gigachad box", -1001923898965],
		24:["BOX WHITE BEAR", -1001918709391], 25:["Box_code", -1001619388393],
		26:["Crypto_POLICE", -1001899781117], 27:["FALCON_CRYPTO", -1001715799457],
		28:["TopCoinChat", -1001596873393],
		30:["Lazragbox", -1001771583894], 31:["Box_Code", -1001619388393], 
		32:["Exist CryptoBox", -1001761501842], 33:["CryptX", -1001913150519],
		34:["CryptoBox_explorers", -1001967726946], 35:["Crypto_SHARK", -1001607486978],
		36:["Double_Crypto_Box", -1001784909674], 37:["Crypto_Anime", -1001984146716],
		38:["Binance_Free_Crypto_Box_Codes", -1001831514584], 39:["B4U Crypto", -1001822421287],
		40:["Mr Crypto", -1001824361872], 41:["Phenix_Chat", -1001633369991],
		42:["Crypto_grinch", -1001697949491], 43:["Agnelia_Group", -1001898195003],
		44:["TBSC", -1001385948381], 45:["Bin_Arabs", -1001874230835], 
		46:["Crypto_Box_Super",-1001602201496], 47:["Gulf_lion_24/7", -1001978966049],
		48:["Crypto_Box_Binance",-1001677216759], 49:["Crypto_Hub", -1001908133833],
		51:["Binance_Crypto_Box", -1001681403762],
		52:["Crypto(Box)", -1002096354640], 53:["Altcoinbox_chat", -1001688397602], 
		54:["Genius_Crypto_Fam", -1001734999276], 55:["GIFT_BOX", -1002068089627],
		56:["CRYPTO_KINGDOM",-1001998730203], 57:["PROBETTING7777",-1001809372291],
		58:["Holi_Box_Chat", -1001599063372], 59:["Crypto_Benz",-1001843343741],
		60:["Beethoven_Bitcoin",-1001418643543], 61:["BTCFREEBOX",-1001862934269],
		62:["Binance_Giveaways",-1001700050770], 63:["COOLBOXXX_BINANCE", -1001637616185],
		64:["Big_Dream_Boxes", -1001995855848], 65:["Star_Crypto_Ukraine_Chat",-1001879280958],
		66:["UBX", -1002105261319], 67:["Crypto_Box_Chat", -1001884201576], 68:["MDN", -1001603950879],
		69:["eCASH BOX",-1001942964314], 70:["Binanox", -1002028548879], 
		71:["Crypto_risebox", "cryptorisebox"], 
		73:["Vanbay", -1001558694540], 74:["Second_Secret", -1001202579329], 
		75:["CoinRain", -1001220129898], 76:["UM_CryptoBox", 1001819613682], 
		77:["Crypto_SLON", -1001856445304], 78:["CryptoZLATA", -1001793039461], 
		79:["Crypto_Water", -1001295028493], 80:["Crypto_Lucky", -1001779612665], 
		81:["Scary_BOX", -1001823867054], 82:["Cream_Swap", -1001962847550], 
		83:["CryptoKraken", -1001680561996], 84:["Crypto_LuckyChat", -1001799171463], 
		85:["ByKaranteli", -1001799038195]}
		
		pops = [8, 16]
		for i in range(2):
			self.boxarr.pop(pops[i])
		self.count = 0; self.x = 0;



	def countdown(self, t):
		num_updates = t
		counter = 0; interval = 1
		
		for _ in range(num_updates + 1):
			rem_min = (num_updates - counter) // 60
			rem_sec = (num_updates - counter) % 60
			print(f"Time left--> {rem_min:02d}:{rem_sec:02d}", end="\r")
			time.sleep(interval); counter += interval



	def file_garb(self, file, text=None, s_text=None):
		directory = os.path.abspath(os.getcwd())
		filepath = os.path.join(directory, file)
		try:
			if os.path.exists(filepath):
				if text is not None:
					logging.info(f"Opening Trashfile\nInvalid code disposed..:{text}")
					with open(filepath, 'a') as dbin:
						dbin.write(text+'\n'); dbin.flush()
				else:
					lines = []; print("<sc_tf>")
					with open(filepath, 'r') as read_bin:
						lines = read_bin.readlines()
					for e in lines:
						if e in s_text:
							logging.info(f"\nFIC:{s_text}") 
							return False
					return True
			else:
				with open(filepath, 'w'):
					pass
		except Exception as e:
			logging.error("<- Error, file_garb ->")
			logging.error(f"{e}, {sys.exc_info()}")



	async def write_to_logs(self, date, filename):
		txt = f'Total opened:{self.open}, Fully claimed:{self.claim}'
		#open the file
		try:
			async with aiofiles.open(filename, 'r') as log:
				lines = await log.readlines()

			for i, line in enumerate(lines):
				if date in line:
					lines[i] = f'Date::<{date}>: {txt}\n'
					return True, lines
			return False 

				
		except FileNotFoundError:
			logging.error("<Couldn't find the file.>\n<Creating a New file>");
			async with aiofiles.open(filename, 'w'):
				logging.info('<File created Successfully>')

			async with aiofiles.open(filename, 'r') as log:
				lines = await log.readlines()

			for i, line in enumerate(lines):
				if date in line:
					lines[i] = f'Date::<{date}>: {txt}\n'
					return True, lines
			return False 

		except Exception as e:
			logging.error('<An Exception occured when writing>')
			logging.error(e, sys.exc_info()); print(traceback.print_exc())


	async def update_logs(self, filename):
		q = await self.write_to_logs(self.today, filename)
		if isinstance(q, tuple):
			async with aiofiles.open(filename, 'w') as file:
				await file.writelines(q[1]); await file.flush();
				await file.close()
				logging.info('<Written to file>')
		else:
			self.open = 0; self.claim = 0;
			txt = f'Total opened:{self.open}, Fully claimed:{self.claim}'
			async with aiofiles.open(filename, 'a') as log:
				await log.write(f'Date::<{self.today}>: {txt}\n')
				await log.flush(); await log.close() 
				print('<Added to file>')

	def write_count(self, date, filename):
		try:
			with open(filename, 'r') as log:
				lines = log.readlines();
			print("Writing counts to file...")
			for line in lines:
				if date in line:
					print('<Found date>')
					nums = re.findall(r'(?<=:)\d+', line);
					return map(int, nums)
			print('Date not found!')
			return 0, 0
					
		except FileNotFoundError:
			logging.error(f'Func_write_count! line 413 in function write_count')
			logging.info('<File Not_found>\n<Creating a New File>');
			with open(filename, 'w'):
				logging.info(f'<File created Successfully>: write_count file.')
			return 0, 0
		except Exception as e:
			print(e, sys.exc_info(), traceback.print_exc())
			return 0, 0
		


class Tel_Fetch(Paste):
	def __init__(self, session_name=None, id_=None, hash_=None):
		super().__init__()
		self.session = session_name; self.api_id = id_
		self.api_hash = hash_; self.used = set()
		self.active = False; self.elapsed = 0
		self.lock = asyncio.Lock()
		self.dictn = enchant.Dict("en_US"); self.invalid = set()
		self.client1 = TelegramClient(self.session, self.api_id, self.api_hash, connection_retries=100)
		#self.client2 = TelegramClient('user2', api_id2, api_hash2)
		self.topcoin_id = 1927685279; self.topcoin = ''
		self.t48 = 5827230154; self.cryboxsuper = 1602201496;

		self.saima = 5691605633; self.bline = 6527848960; self.earlyriv = 5829802824;
		self.nothang = 5569742554; self.agnelia_id = 5833269780; self.phenix = 2045299958
		self.myid = 2092644299; self.mysid = 2032087917; self.sheikhbd = 1838514169
		self.myid2 = 985086727; self.erman = 6647720035;
		self.altcoinid = 1974878554; self.elza = 5704133938; self.djkv = 6660985801
		self.nany = 1042763214; self.gtiya = 5698006635; self.g18_11 = 6232447650
		self.hophop = 5550955249; self.nn = 1474913955

		self.pids = {self.topcoin_id:"topcoin", self.saima:"photo", self.bline:"photo", 
		self.agnelia_id:"agnelia", self.phenix:"phenix_chat", 
		self.myid:"me", self.mysid:"me", self.myid2:"me"}

		self.maskers = {self.topcoin_id:"topcoinchat", self.nothang:"cryptotree", 
		self.t48:"box_tigre", self.cryboxsuper:"cryptoboxsuper", self.sheikhbd:"sheikhbd", 
		self.altcoinid:"altcoinchat", self.elza:"btcfreebox, elza", self.djkv:"dj", self.nany:"btcfreebox, nany"
		,self.earlyriv:"earlyrivo", self.erman:"cryptokingdom", self.gtiya:"G_tiya", 
		self.g18_11:"G_18_11", self.hophop:"cryptokingdom, hophop", self.nn:"cryptokingdom, nn"}
		
		self.chatnames = {"Mr Crypto":"photo", "sheikhbd1box":"sheikhbd", "TopCoinChat":"topcoin", 
		"Crypto(Box)":"crypto(box)"}

		

	def sign(self, func):
		 return signature(func)

	async def fetch_codes(self, file, set_):
		arr = []; set_ = set()
		try:
			with open(file, 'r') as codes:
				for line in codes:
					arr.append(line[:-1])
			arr = arr[::-1] #To fetch most current ones
			for i in range(50):
				try:	
					e = arr[i]; set_.add(e)
				except IndexError:
					pass

			logging.info(f"{set_}")
			arr = arr[::-1] #To paste most current ones.
			with open(file, 'w') as codes:
				codes.write(''); codes.flush(); codes.close()

			async with aiofiles.open(file, 'a') as codes:
				for each in arr:
					await codes.write(each+'\n'); await codes.flush()
				await codes.close()

		except FileNotFoundError:
			logging.error('<- Fetch codes ->\nNo such file exists:: line 465 in function fetch_codes')
			logging.info('<File Not_found>\n<Creating a New File>');
			with open(file, 'w'):
				logging.info(f'<File created Successfully>: Opened_codes file.')
		except Exception as e:
			print(e, sys.exc_info())



	async def send_message(self, user:str, text:str):
		try:
			await self.client1.start()
			await asyncio.create_task(self.client1.send_message(user, text))
		except Exception as e:
			logging.error("<Sending message>: line 514")
			logging.error(f"{e}, {sys.exc_info()}: line 514")


	async def _call(self):
		print("Calling...")
		chat_ids = [self.boxarr[n][1] for n in self.boxarr]
		chat_names = [self.boxarr[n][0] for n in self.boxarr]

		async def find_maskers(checktype, message, chatname):
			try:
				print('Checking:', chatname, '->', [f'id:{checktype}', 
					f'firstname:{message.sender.first_name}'])
			except AttributeError as e:
				pass
			
			neg = ['Genius_Crypto_Fam', 'Binance_Free_Crypto_Box_Codes']
			try:
				who = self.maskers[checktype] if checktype else chatname
				if chatname not in neg:
					await self.send_message(-1002092644299, f"From {who}")
					if message.photo or message.media:
						await self.client1.send_file(-1002092644299, message.photo if message.photo else message.media)
					else:
						asyncio.create_task(self.send_message(-1002092644299, f"{message.text}"))
			except KeyError:
				pass
			except Exception as e:
				asyncio.create_task(self.send_message(-1002092644299, f"{'Photo' if message.photo else 'Gif/Sticker'}"))


			

		async def Typeof(checktype, message, chatname):
			botpoisoners = [self.nothang, 6216891439, 1616507228] #5724683203  
			botpoisonerschat = ['Genius_Crypto_Fam']; isbot = False
			try:
				isbot = message.sender.bot
			except AttributeError:
				isbot = False
	
			await find_maskers(checktype, message, chatname)
			if checktype:
				try:
					await self.extract_codes(self.pids[checktype], message, chatname)
				except KeyError as e:
					#print("<checkype in Typeof>:", e)
					if (checktype not in botpoisoners) and (not isbot):
						await self.extract_codes("main", message, chatname)
			else:
				try:
					await self.extract_codes(self.chatnames[chatname], message, chatname)
				except KeyError as e:
					#print("<!checktype in Typeof>:", e)
					if chatname not in botpoisonerschat:
						await self.extract_codes("main", message, chatname)
		
		async def on_new_message(event, chat_name:str):
			await asyncio.sleep(0.05256); 
			try:
				message = event.message; Peerid = message.sender
				checktype = message.sender.id if Peerid else False
				await Typeof(checktype, message, chat_name)
				len_users = loginbot.users; tsks = []
				for each in len_users:
					tsks.append(asyncio.create_task(self.is_active(each)))
				await asyncio.gather(*tsks)
			
			except loginbot.apihelper.ApiTelegramException as e:
				print(f"From_Bot\n{e}")
			except Exception as e:
				print(e, sys.exc_info())
				print(f"<Exception while fetching real-time message>")

		for i in range(len(chat_ids)):
			self.client1.add_event_handler(
				lambda e, name=chat_names[i]: on_new_message(e, name), 
				events.NewMessage(chats=chat_ids[i]))

		await self.client1.run_until_disconnected()


	async def is_active(self, id_):
		activeuser = loginbot.users[id_]

		iswait = activeuser["waitTime"]
		if iswait and (not activeuser['login']): 
			loginbot.bot.send_message(id_, "Session Expired👻"); activeuser["waitTime"] = False 
			await asyncio.sleep(2000); activeuser["waitTime"] = True
		else:
			await self.process_message(id_)


	async def process_message(self, iD):
		try:
			activeuser = loginbot.users[iD];
			#activeuser['queue'] = self.asyc_q
			
			dup = self.asyc_q
			while not dup.empty():
				item = await dup.get(); await activeuser['queue'].put(item)

			queue = activeuser['queue']; myset = activeuser['set']; isuser_loggedin = activeuser['login']
			
			if isuser_loggedin:
				activeuser["waitTime"] = False; self.rot += 1
				asyncio.create_task(self.load_queue(iD, activeuser, queue, myset))#for multiple users
		except Exception as e:
			print(f"{e}, {sys.exc_info()}")

	
	async def load_queue(self, iD, activeuser, queue, myset):
		print("Load Queue:", iD); proxylen = len(loginbot.proxies)
		self.rot %= proxylen; proxy = loginbot.proxies[self.rot]
		print(f"Using Proxy [{proxy}]")
		while not queue.empty():
			await asyncio.sleep(0.1)
			k = await queue.get(); fg = self.file_garb("Invalid_codes.txt", s_text=k)
			if (k not in myset) and fg:
				asyncio.create_task(
					self.client1(functions.messages.SetTypingRequest(
						-1001862934269, types.SendMessageTypingAction())))
				
				valid = await loginbot.Login.attemptcode(activeuser['session'], k, iD, '')

				if valid != None:
					logouttime = datetime.datetime.now(); hr = logouttime.hour;
					mins = logouttime.minute; secs = logouttime.second; 
					if valid["message"] == "TypeErr":
						print(valid["e"])
					elif valid["message"] == "Please try":
						activeuser["login"] = False
						loginbot.bot.send_message(iD, f"[Oops🙊]\n{valid['e']}\n @{hr}:{mins:02d}:{secs:02d} 🙄")
					elif valid["message"] == "Bot":  
						activeuser["login"] = False;
						loginbot.bot.send_message(iD, f"{valid['e']}\n@ {hr}:{mins:02d}:{secs:02d}")
				myset.add(k); 
		self.asyc_q = asyncio.Queue()


	async def check_client(self):
		"""my_channel_id = -1002092644299"""
		try:
			isconn = self.client1.is_connected(); isauth = self.client1.is_user_authorized()
			if isconn and await isauth:
				print(f"{Fore.GREEN}[+]Client Is active.{Style.RESET_ALL}")
				bottask = threading.Thread(target=loginbot.main)
				bottask.start()
				task_one = asyncio.create_task(self.run_true()); task_two = asyncio.create_task(self._call())
				await task_one; await task_two;
				#self.open, self.claim = self.write_count(self.today, "Counts.txt")
			else:
			 	print(f"{Fore.RED}[-]Not connected!{Style.RESET_ALL}")
			 	print(f"{Fore.RED}[+]Trying to start client.{Style.RESET_ALL}")
			 	reply = int(input("Select device type\n[1]Pc\n[2]Mobile\n:"))
			 	if reply == 1:
			 		await self.client1.start(); await self.check_client()
			 	else:
			 		await self.client1.connect();
			 		phone = input("Enter your telegram phone no. : ")
			 		await self.client1.send_code_request(phone);
			 		code = input("Enter the code received: ")
			 		try:
			 			await self.client1.sign_in(phone, code)
			 			await self.check_client()
			 		except SessionPasswordNeededError:
			 			password = getpass("Enter your password: ")
			 			try:
			 				await self.client1.sign_in(password=password)
			 				await self.check_client()
			 			except Exception as e:
			 				print("Error:", e)
		except Exception as e:
			print(e);
			
	async def run_true(self):
		print(f"{Fore.BLUE}Running...{Style.RESET_ALL}")
		while True:
			dtime = datetime.datetime.now(); self.today = str(dtime.date());
			if loginbot.items:
				await loginbot.create_session(*loginbot.items)
				loginbot.items = []
			ctime = dtime.time(); hour = ctime.hour
			filesz = os.path.getsize('TGLOG.log')
			if filesz >= 50 * 1024:
				with open('TGLOG.log', 'w') as file:
					file.write('')
			await asyncio.sleep(0)

	async def strict_check(self, code, l):
		addword = ''
		for each in code:
			addword += each
			if len(addword) >= l:
				if self.dictn.check(addword):
					return True
		return False


	def filter_text(self, pat, text):
		splitted = re.sub(pat, ' ', text).split(' ')
		for each in splitted:
			each = each.strip(); 
			mat = re.findall(r'(^(?=.*[A-Za-z])[A-Z\da-z]{8})(?!.+)', each)
			yield mat.pop() if mat else ''

	def reset_pattern(self, chat, checkfor, maintext):
		
		def reset_topcoin(word, text):
			if word in text:
				print("Resetting for Topcoin"); self.topcoin = ''
		
		
		resetchats = {"TopCoinChat":reset_topcoin}
		resetchats[chat](checkfor, maintext)
	

	def swap(self, m):
		char = m.group(0)
		if char == '0':
			return 'O'
		return '0'

		

	async def extract_codes(self, func_name, t, chatname):
		real_text = t.text;  p = t.photo

		async def main(text):
			print("Using main_extract..")
			match = self.filter_text(r'[^A-Z\d]', text)
			if 'bybit' in text.lower():
				print("ByBit code.")
			elif 'http' in text.lower():
				print("Link")
			else:
				for c in match:
					if c not in self.used and c != '':
						swd = await self.strict_check(c, 4)
						if not swd:
							print([c]); await self.asyc_q.put(c)

		async def Agnelia(text):
			print("Using Agnelia bot..")
			match = self.filter_text(r'[^A-Z\da-z]', text)
			for c in match:
				if c != '':
					print([c]); await self.asyc_q.put(c)

		async def Me(text):
			print('Trying I.')
			match = self.filter_text(r'[^A-Z\da-z@]', text)
			for c in match:
				if chatname == 'My_Channel' and ('gg' in text):
					if c != '' and (not self.dictn.check(c)):
						await self.asyc_q.put(c.upper())
				elif chatname != 'My_Channel':
					if c != '' and (not self.dictn.check(c)):
						await self.asyc_q.put(c.upper())
				


		async def Sheikhbd(text):
			def replc(obj):
				char = obj.group(0);
				objs = {'🕐':'1', '🕑':'2', '🕒':'3', '🕓':'4', '🕔':'5', 
				'🕕':'6', '🕖':'7', '🎱':'8','🕘':'9'}
				try:
					return objs[char]
				except KeyError:
					pass
			async def type1(text):
				ref_txt = re.sub(r'[🕐🕑🕒🕓🕔🕕🕖🎱🕘]', replc, text.strip())
				mat = re.findall(r'(^(?=.*[A-Z])[A-Z\d]{8})(?!.+)', ref_txt)
				if mat:
					self.asyc_q.put(mat.pop())
			asyncio.create_task(main(text)); await type1(text)


		async def Phenix_chat(text):
			print("Using Phenix Chat..")
			raw_text = re.split(r'[()]', text)
			phenix_dict = {i:chr(i+64) for i in range(1, 26)}
			if '(' in text and ')' in text:
				for i in range(len(raw_text)):
					try:
						raw_text[i] = phenix_dict[eval(raw_text[i])]
					except:
						pass
				ref = ''.join(raw_text)
				mat = re.findall(r'(^(?=.*[A-Z])[A-Z\d]{8})(?!.+)', ref)
				if mat:
					await self.asyc_q.put(mat.pop())
			elif 'instead' in text.lower():
				print([text])




		async def open_photo():
			print("Opening photo for code..")
			photo_name = await self.client1.download_media(p, file=download_picture_path)
			
			asyncio.create_task(delete_photo(photo_name))
		
		async def photo_text(text):
			if p:	
				asyncio.create_task(open_photo())
			if text:
				await main(text)
		
		async def delete_photo(p):
			print(p)
			if os.path.exists(p):
				os.remove(p); print("Picture deleted!")
			else:
				print("Try to configure picture path.")


		async def topcoin(text):
			print("Trying Topcoin..")

			async def type1(text):
				print("Using topcoin1..")
				splitted = re.sub(r'[^A-Z\d]', ' ', text).split(' ')
				for each in splitted:
					each = each.strip(); le = len(each)
					if self.topcoin == '' and le == 5:
						self.topcoin += each
					elif self.topcoin and each.isalnum():
						self.topcoin += each
					
					print("Current code:", self.topcoin)
					mat = re.findall(r'(^(?=.*[A-Z])[A-Z\d]{8})(?!.+)', self.topcoin)
					if mat:
						print(f"Match from Topcoin:{mat}")
						await self.asyc_q.put(mat.pop()); self.topcoin = ''
			
			await type1(text)

		async def crypto_box(text):
			def replc(obj):
				char = obj.group(0);
				objs = {"🍎":"A", "🚴‍♂️":"B", "🐱":"C", "🌼":"D", "🌟":"E", "🍟":"F", "🎸":"G", "🏡":"H", 
				"👀":"I", "🤹‍♂️":"J", "🔑":"K",
				"📚":"L", "🌊":"M", "🚶‍♀️":"N", "🌍":"O", "🍕":"P", "🤖":"Q", "🚀":"R", "🌻":"S", "🍵":"T", "💤":"U",
				"🎻":"V", "🌄":"W", "❌":"X", "🧀":"Y", "🦓":"Z", "🎲":"0", "🕐":"1",
				"🎰":"2", "🔮":"3", "🎈":"4","🌈":"5", "🎯":"6", "🍀":"7", "🎳":"8", "🔥":"9"}
				try:
					return objs[char]
				except KeyError:
					pass
			async def type1(text):
				ref_txt = re.sub(r'[🍎🚴‍♂️🐱🌼🌟🍟🎸🏡👀🤹‍♂️🔑📚🌊🚶‍♀️🌍🍕🤖🚀🌻🍵💤🎻🌄❌🧀🦓🎲🕐🎰🔮🎈🌈🎯🍀🎳🔥]', replc, text.strip())
				mat = re.findall(r'(^(?=.*[A-Z])[A-Z\d]{8})(?!.+)', ref_txt)
				if mat:
					await self.asyc_q.put(mat.pop())

			asyncio.create_task(main(text)); await type1(text)


		
		cfors = {"TopCoinChat":"thank"}
		tx = ''.join(re.split(r'[^\w]', real_text)).lower()
		try:
			self.reset_pattern(chatname, cfors[chatname], tx)
		except KeyError:
			pass
		finally:
			#photo is being changed to main tempoarily.
			func_names = {"topcoin":topcoin, "photo":main, 
			"main":main, "agnelia":Agnelia, "phenix_chat":Phenix_chat, 
			"me":Me, "sheikhbd":Sheikhbd, "crypto(box)":crypto_box}
			await func_names[func_name](real_text if real_text else '')
			

#Start program
Run_client = Tel_Fetch('_session_', api_id, api_hash)#reset
async def run_telethon():
	await Run_client.check_client()

def start_process():
	asyncio.run(run_telethon())
start_process()
