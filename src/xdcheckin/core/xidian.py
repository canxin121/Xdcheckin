# -*- coding: utf-8 -*-

from threading import Thread
from xdcheckin.core.chaoxing import Chaoxing

from base64 import b64decode, b64encode
from Crypto.Cipher.AES import new as AES_new, block_size as AES_block_size, MODE_CBC as AES_MODE_CBC
from Crypto.Util.Padding import pad
from io import BytesIO
from PIL.Image import open
from re import search
from requests import Response, Session
from requests.exceptions import RequestException
from time import time

class IDSSession:
	requests_session = secrets = service = logined = None
	config = {
		"requests_headers": {
			"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
		}
	}

	def __init__(self, service: str = ""):
		"""Initialize an IDS Session.
		:param service: The sso service for redirection.
		"""
		if self.logined:
			return
		self.requests_session, self.secrets, self.service = Session(), {}, service

	def get(self, url: str = "", params: dict = {}, cookies: dict = None, headers: dict = None, verify: bool = False):
		"""Wrapper for requests.get().
		:param url: URL.
		:param params: Parameters.
		:param cookies: Cookies. Overrides existing cookies.
		:param headers: Headers. Overrides existing headers.
		:param verify: SSL certificate verification toggle. False by default.
		:return: Response.
		"""
		try:
			res = self.requests_session.get(url, params = params, cookies = cookies, headers = headers or self.config["requests_headers"], verify = False)
			assert res.status_code in (200, 500), res.status_code
		except AssertionError as e:
			res = Response()
			res.status_code, res._content = e, b"{}"
		except RequestException:
			res = Response()
			res.status_code, res._content = 404, b"{}"
		finally:
			return res

	def post(self, url: str = "", data: dict = {}, params: dict = {}, cookies: dict = None, headers: dict = None, verify: bool = False, cache: bool = False):
		"""Wrapper for requests.post().
		:param url: URL.
		:param data: Data.
		:param params: Parameters.
		:param cookies: Cookies. Overrides existing cookies.
		:param headers: Headers. Overrides existing headers.
		:param verify: SSL certificate verification toggle. False by default.
		:return: Response.
		"""
		try:
			res = self.requests_session.post(url, data = data, params = params, cookies = cookies, headers = headers or self.config["requests_headers"], verify = False)
			assert res.status_code in (200, 500), res.status_code
		except AssertionError as e:
			res = Response()
			res.status_code, res._content = e, b"{}"
		except RequestException:
			res = Response()
			res.status_code, res._content = 404, b"{}"
		finally:
			return res

	def login_prepare(self):
		"""Prepare for login verification.
		:return: Base64 encoded captcha background and slider image string.
		"""
		url1 = "https://ids.xidian.edu.cn/authserver/login"
		params1 = {
			"service": self.service
		}
		url2 = "https://ids.xidian.edu.cn/authserver/common/openSliderCaptcha.htl"
		params2 = {
			"_": 0
		}
		ret = {
			"big_img_src": "",
			"small_img_src": ""
		}
		res1 = self.get(url1, params = params1)
		if not res1.status_code == 200:
			return ret
		s = search(r"\"pwdEncryptSalt\" value=\"(.*?)\".*?\"execution\" value=\"(.*?)\"", res1.text)
		params2["_"] = str(int(1000 * time()))
		res2 = self.get(url2, params = params2)
		if not res1.status_code == 200:
			return ret
		ret.update({
			"big_img_src": res2.json()["bigImage"],
			"small_img_src": res2.json()["smallImage"]
		})
		self.secrets.update({
			"login_prepare_salt": s.group(1),
			"login_prepare_execution": s.group(2)
		})
		return ret

	def login_finish(self, account: dict = {"username": "", "password": "", "vcode": ""}):
		"""Verify and finish logging in.
		:param account: Username, password and verification code (a.k.a. slider offset).
		:return Cookies and login state:
		"""
		def _encrypt_aes(msg: str = "", key: str = ""):
			enc = AES_new(key.encode("utf-8"), AES_MODE_CBC, b"xidianscriptsxdu").encrypt(pad(4 * b"xidianscriptsxdu" + msg.encode("utf-8"), AES_block_size))
			return b64encode(enc).decode("utf-8")

		url1 = "https://ids.xidian.edu.cn/authserver/common/verifySliderCaptcha.htl"
		data1 = {
			"canvasLength": 280,
			"moveLength": account["vcode"]
		}
		ret = {
			"cookies": None,
			"logined": False
		}
		res1 = self.post(url1, data = data1)
		if not res1.status_code == 200 and res1.json()["errorCode"] == 1:
			return ret
		url2 = "https://ids.xidian.edu.cn/authserver/login"
		data2 = {
			"username": account["username"],
			"password": _encrypt_aes(account["password"], self.secrets["login_prepare_salt"]),
			"captcha": "",
			"_eventId": "submit",
			"cllt": "userNameLogin",
			"dllt": "generalLogin",
			"lt": "",
			"execution": self.secrets["login_prepare_execution"]
		}
		params2 = {
			"service": self.service
		}
		res2 = self.post(url2, data = data2, params = params2)
		if not res2.status_code == 200:
			return ret
		ret.update({
			"cookies": self.requests_session.cookies,
			"logined": True
		})
		return ret

class Newesxidian:
	"""XDU exclusive APIs for classroom livestreams.
	"""
	chaoxing_session = logined = None

	def __init__(self, chaoxing: Chaoxing = None):
		if self.logined or not chaoxing.logined or not chaoxing.cookies.get("fid", 0) == "16820":
			return
		self.logined, self.chaoxing_session = True, chaoxing

	def livestream_get_url(self, livestream: dict = {"live_id": ""}):
		"""Get livestream URL.
		:param livesteam: Live ID in dictionary.
		:return: Livestream URL, live ID and device ID (placeholder). URL will fallback to replay URL for non-ongoing live IDs.
		"""
		url = "https://newesxidian.chaoxing.com/live/getViewUrlHls"
		params = {
			"liveId": livestream["live_id"]
		}
		res = self.chaoxing_session.get(url = url, params = params, expire = 86400)
		return {
			"url": res.text,
			"live_id": livestream["live_id"],
			"device": ""
		}

	def livestream_get_live_url(self, livestream: dict = {"live_id": "", "device": ""}):
		"""Get livestream URL.
		:param livestream: Live ID (unused if device ID is present) or device ID in dictionary.
		:return: Livestream URL, live ID (placeholder if not given) and device ID.
		"""
		url1 = "http://newesxidian.chaoxing.com/live/listSignleCourse"
		params1 = {
			"liveId": livestream.get("live_id", "")
		}
		url2 = "http://newesxidian.chaoxing.com/live/getViewUrlNoCourseLive"
		params2 = {
			"deviceCode": livestream.get("device", ""),
			"status": 1
		}
		if not livestream.get("device"):
			res1 = self.chaoxing_session.get(url = url1, params = params1, expire = 86400)
			data = res1.json() or []
			for lesson in data:
				if str(lesson["id"]) == livestream["live_id"]:
					params2["deviceCode"] = lesson["deviceCode"]
					break
		res2 = self.chaoxing_session.get(url = url2, params = params2, expire = 86400)
		return {
			"url": res2.text,
			"live_id": params1["liveId"],
			"device": params2["deviceCode"]
		}

	def curriculum_get_curriculum(self):
		"""Get curriculum with livestream URLs.
		:return: Chaoxing curriculum with livestream URL, live ID and CCTV device ID for lessons.
		"""
		def _get_livestream_wrapper(class_id: str = "", live_id: str = ""):
			curriculum["lessons"][class_id]["livestream"] = self.livestream_get_live_url(livestream = {"live_id": live_id})
		url = "https://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage"
		params = {
			"fid": 16820,
			"userId": self.chaoxing_session.cookies["UID"],
			"termYear": 0,
			"termId": 0,
			"week": 0
		}
		curriculum = self.chaoxing_session.curriculum_get_curriculum()
		params.update({
			"termYear": curriculum["details"]["year"],
			"termId": curriculum["details"]["semester"],
			"week": curriculum["details"]["week"]
		})
		res = self.chaoxing_session.get(url = url, params = params, expire = 86400)
		data = res.json() or []
		threads = tuple(Thread(target = _get_livestream_wrapper, kwargs = {"class_id": class_id, "live_id": live_id}) for class_id, live_id in {str(lesson["teachClazzId"]): str(lesson["id"]) for lesson in data}.items())
		tuple(thread.start() for thread in threads)
		tuple(thread.join() for thread in threads)
		return curriculum

if __name__ == "__main__":
	"""Test IDS Login.
	"""
	ids = IDSSession(service = "https://learning.xidian.edu.cn/cassso/xidian")
	print("start prep")
	prep = ids.login_prepare()
	print("end prep", prep)
	img = open(BytesIO(b64decode(prep["big_img_src"])))
	img.show()
	vcode = int(input("vcode: ")) * 280 / img.width
	account = {"username": f"{input('username: ')}", "password": f"{input('password: ')}", "vcode": vcode}
	print("start finish", account)
	finish = ids.login_finish(account = account)
	print("end finish", finish)
