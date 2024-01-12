import requests
import json, sys
from colorama import Fore, Style, init
from urllib import parse
from random import randint
import time
import os, logging
init()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
dev_info = "eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjczMCwxMjk4IiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiNjkyLDEyOTgiLCJzeXN0ZW1fdmVyc2lvbiI6IldpbmRvd3MgMTAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6ImVuLUdCIiwidGltZXpvbmUiOiJHTVQrMDE6MDAiLCJ0aW1lem9uZU9mZnNldCI6LTYwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6MTIxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTIxLjAiLCJsaXN0X3BsdWdpbiI6IlBERiBWaWV3ZXIsQ2hyb21lIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlcixNaWNyb3NvZnQgRWRnZSBQREYgVmlld2VyLFdlYktpdCBidWlsdC1pbiBQREYiLCJjYW52YXNfY29kZSI6IjkwOTQwNjU1Iiwid2ViZ2xfdmVuZG9yIjoiR29vZ2xlIEluYy4gKEFNRCkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChBTUQsIFJhZGVvbiBIRCAzMjAwIEdyYXBoaWNzIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCkiLCJhdWRpbyI6IjM1Ljc0OTk2ODIyMzI3Mzc1NCIsInBsYXRmb3JtIjoiV2luMzIiLCJ3ZWJfdGltZXpvbmUiOiJBZnJpY2EvTGFnb3MiLCJkZXZpY2VfbmFtZSI6IkZpcmVmb3ggVjEyMS4wIChXaW5kb3dzKSIsImZpbmdlcnByaW50IjoiYTgzNzNhZTdmZGE2NzY3ZDkwODBkMGE0YmY0ODVhYzQiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIifQ=="

host = "www.binance.com"
origin = "https://www.binance.com"
referrer = "https://www.binance.com/en/my/wallet/account/payment/cryptobox"
sec_fet_mode = "cors"
sec_fet_site = "same-origin"

coins = {}

class Authenticate_Login:
	def __init__(self):
		self.session = requests.Session()
		self.header = {"User-Agent":user_agent,
		"clienttype": "web", "content-type": "application/json", 'Accept-Language':'en-US,en;q=0.9',
		"device-info":dev_info, "Host":host, "Origin":origin, "lang":"en",
		"Sec-Fet-Mode":sec_fet_mode, "Sec-Fet-Site":sec_fet_site, "Referer":referrer} 

	def opened_cfile(self, file, text, condition=True):
		directory = os.path.abspath(os.getcwd())
		filepath = os.path.join(directory, file)
		try:
			if os.path.exists(filepath):
				if condition:
					logging.info("\nThrowing used codes into file..")
					with open(filepath, 'a') as opened:
						opened.write(text+'\n')
			else:
				with open(filepath, 'w'):
					pass
		except Exception as e:
			print("<- Opened Cfile ->")
			print(e, sys.exc_info())

	def file_garb(self, file, text=None, s_text=None):
		directory = os.path.abspath(os.getcwd())
		filepath = os.path.join(directory, file)
		try:
			if os.path.exists(filepath):
				if text is not None:
					logging.info(f"{Fore.RED}Opening Trashfile\nInvalid code disposed..:{text}{Style.RESET_ALL}")
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



	def check_loginstatus(self, CSRF, COOKIE, user_session):
		url = "https://www.binance.com/bapi/pay/v1/private/binance-pay/account/get-self-status"
		csrf_token = CSRF; cookies = COOKIE
		self.header["csrftoken"] = csrf_token; self.header["Cookie"] = cookies
		user_session.headers.update(self.header)
		try:
			response = user_session.post(url)
			if response.status_code == 200:
				text = json.loads(response.text);
				print(f"{Fore.GREEN}Login Successfully...{Style.RESET_ALL}");
				print(); data = text["data"]
				for key, value in data.items():
					print(f"{key}: {value}")
				return {"message":"Login Successful..", "success":True, 
				"userId":data["userId"], "nickname":data["nickname"]}
			else:
				return json.loads(response.text)
		except Exception as e:
			print(e)
			return {"message":e, success:False}

	def attemptcode(self, user_session, code, id_):
		print(f"{Fore.BLUE}Attempting code..{Style.RESET_ALL}")
		url = "https://www.binance.com/bapi/pay/v1/private/binance-pay/gift-box/code/query"
		payload = {"channel":"DEFAULT", "grabCode":code}
		try:
			time.sleep(0.11)
			response = user_session.post(url, json=payload)
			response.raise_for_status()
			if response.status_code == 200:
				print(f"{Fore.GREEN}Posted code successfully...{Style.RESET_ALL}")
				text = response.text
				self.process_code(user_session, text, payload, id_)
			else:
				print("STATUS_CODE:",response.status_code, "\n", response.text)
				return json.loads(response.text)
		except Exception as e:
			print(e, sys.exc_info())
			return {"message":e, success:False}


	def process_code(self, user_session, obj, load, id_):
		print(f"{Fore.GREEN}Processing code..{Style.RESET_ALL}")
		json_dict = json.loads(obj)
		data = json_dict["data"]; success = json_dict["success"]
		if success:
			isgrab = data["grabbed"]
			if isgrab:
				nickname = data["payerNickname"]; slots = data["totalCount"]
				print(f"{Fore.LIGHTCYAN_EX}Payer_Nickname:{nickname}\nSlots:{slots}{Style.RESET_ALL}")	
				print(f"\n{Fore.LIGHTCYAN_EX}Already claimed...{Style.RESET_ALL}")
			else:
				self.grab_code(user_session, load, id_)
		else:
			errtext = json_dict['message']
			if "Invalid code" in errtext:
				self.file_garb("Invalid_codes.txt", text=load['grabCode'])
			print(f"{Fore.RED}{errtext}{Style.RESET_ALL}")

	def grab_code(self, user_session, load, id_, captcha=False):
		print(f"{Fore.BLUE}Grabbing code in a bit..{Style.RESET_ALL}")
		time.sleep(0.05)
		url = "https://www.binance.com/bapi/pay/v1/private/binance-pay/gift-box/code/grabV2"
		if not captcha:
			payload = load; payload["scene"] = None
			print(payload)
			response = user_session.post(url, json=payload)
			if response.status_code == 200:
				text = response.text
				self.finalize_grab(user_session, text, id_, payload['grabCode'])
			else:
				print("STATUS_CODE:",response.status_code, "\n", response.text)
		else:
			payload = {"captchaChallenge":"", "captchaToken":"", "channel":"DEFAULT", "scene":None}


	def finalize_grab(self, user_session, obj, id_, code):
		print(f"{Fore.BLUE}Finalizing grab..{Style.RESET_ALL}")
		json_dict = json.loads(obj);
		data = json_dict["data"]; success = json_dict["success"]
		print(json_dict)
		if success:
			currency = data['currency']; amount = data['grabAmount']
			if currency not in coins:
				coins[id_][currency] = amount
			else:
				coins[id_][currency] += amount
			self.opened_cfile('Opened_codes.txt', code)
			print(f"{Fore.YELLOW}Currency: {data['currency']}, Amount: {data['grabAmountStr']}{Style.RESET_ALL}")
		else:
			print(json_dict["message"])
			return self.get_captcha(user_session, data['validateId'])

	def get_captcha(self, user_session, vId):
		url = "https://www.binance.com/bapi/composite/v1/public/antibot/getCaptcha"
		payload = {"bizId":"crypto_box_claim", "sv":"20220906", "lang":"en", 
		"securityCheckResponseValidateId":vId, "clientType":"web"}
		try:
			response = user_session.post(url, json=payload)
			if response.status_code == 200:
				text = json.loads(response.text)
				return self.solve_captcha(user_session, text)
			else:
				print("STATUS_CODE:",response.status_code, "\n", response.text)
		except Exception as e:
			print(e, sys.exc_info())


	def solve_captcha(self, user_session, load):
		print(f"{Fore.RED}Attempting to solve captcha..{Style.RESET_ALL}")
		print(load)
		return {"success":False, "message":"[Captcha!!😡], Retry->(Session/New Session)"}


Login = Authenticate_Login()

#ANTIBOT_CHECK
#bizId=crypto_box_claim&sv=20220906&lang=en&securityCheckResponseValidateId=217d663ccd9b4101a61d61e71ea62411&clientType=web
#https://www.binance.com/bapi/composite/v1/public/antibot/getCaptcha