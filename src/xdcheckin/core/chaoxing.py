# -*- coding: utf-8 -*-

from ast import literal_eval as _literal_eval
from asyncio import create_task as _create_task, gather as _gather, \
Semaphore as _Semaphore
from json import dumps as _dumps
from random import uniform as _uniform
from re import findall as _findall, search as _search, split as _split, \
DOTALL as _DOTALL
from time import time as _time
from xdcheckin.util.chaoxing_captcha import \
generate_secrets as _generate_secrets
from xdcheckin.util.encryption import encrypt_aes as _encrypt_aes
from xdcheckin.util.session import CachedSession as _CachedSession
from xdcheckin.util.time import strftime as _strftime

class Chaoxing:
	"""Common Chaoxing APIs.
	"""
	config = {
		"requests_headers": {
			"User-Agent":
				"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit"
				"/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 M"
				"obile Safari/537.36 com.chaoxing.mobile/ChaoXi"
				"ngStudy_3_6.1.0_android_phone_906_100"
		},
		"requests_cache_enabled": True,
		"chaoxing_course_get_activities_courses_limit": 32,
		"chaoxing_course_get_activities_workers": 16,
		"chaoxing_checkin_location_address_override_maxlen": 0,
		"chaoxing_checkin_location_randomness": True
	}
	__async_ctxmgr = __session = None
	logined = False
	fid = uid = 0
	__account = {}
	courses = {}

	def __init__(
		self, username: str = "", password: str = "", cookies = {},
		config: dict = {}
	):
		"""Create a Chaoxing instance and login.
		:param username: Chaoxing username. \
		Unused if ``cookies`` is given.
		:param password: Chaoxing password. \
		Unused if ``cookies`` is given.
		:param cookies: Cookies from previous login. Overrides \
		``username`` and ``password`` if given.
		:param config: Configurations.
		:return: None.
		"""
		if not self.__async_ctxmgr is None:
			return
		assert (username and password) or cookies
		assert type(config) is dict
		self.config.update(config)
		self.__session = _CachedSession(
			headers = self.config["requests_headers"],
			cache_enabled = self.config["requests_cache_enabled"]
		)
		self.__account = {
			"username": username, "password": password,
			"cookies": cookies
		}

	async def __aenter__(self):
		if not self.__async_ctxmgr is None:
			return self
		self.__async_ctxmgr = True
		await self.__session.__aenter__()
		username, password, cookies = self.__account.values()
		if cookies:
			self.name, cookies, self.logined = \
			(await self.login_cookies(account = self.__account)).values()
		login_funcs = (
			self.login_username_fanya, self.login_username_v3,
			self.login_username_v5, self.login_username_v25,
			self.login_username_v2, self.login_username_v11,
			self.login_username_xxk, self.login_username_mylogin1
		)
		if not self.logined and username and password:
			for func in login_funcs:
				self.name, cookies, self.logined = \
				(await func(account = self.__account)).values()
				if self.logined:
					break
		if self.logined:
			if "fid" in cookies:
				self.fid = cookies["fid"].value
			self.__session.cookies = cookies
			self.uid = cookies["UID"].value
			self.courses = await self.course_get_courses()
		return self

	async def __aexit__(self, *args, **kwargs):
		if self.__async_ctxmgr != True:
			return
		await self.__session.__aexit__(*args, **kwargs)
		self.__async_ctxmgr = False

	async def get(self, *args, **kwargs):
		return await self.__session.get(*args, **kwargs)

	async def post(self, *args, **kwargs):
		return await self.__session.post(*args, **kwargs)

	async def login_username_v2(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via V2 API.
		:param account: Username and password in dictionary.
		:return: Name, cookies and login state.
		"""
		url = "https://passport2.chaoxing.com/api/v2/loginbypwd"
		params = {
			"name": account["username"], "pwd": account["password"]
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.get(url = url, params = params)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			data = await res.json(content_type = None)
			ret.update({
				"name": data["realname"],
				"cookies": res.cookies, "logined": True
			})
		return ret

	async def login_username_v3(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via V3 API.
		:param account: Same as ``login_username_v2()``.
		:return: Name (``""``), cookies and login state.
		"""
		url = "http://v3.chaoxing.com/vLogin"
		data = {
			"userNumber": account["username"],
			"passWord": account["password"]
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.post(url = url, data = data)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return ret

	# tofix
	async def login_username_v5(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via V5 API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v2()``.
		"""
		url = "https://v5.chaoxing.com/login/passportLogin"
		data = {
			"userNumber": account["username"],
			"passWord": account["password"]
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.post(
			url = url, data = _dumps(data), headers = {
				**self.__session.headers,
				"Content-Type": "application/json;charset=utf-8"
			}
		)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			data = await res.json()
			ret.update({
				"name": data["data"]["realname"],
				"cookies": res.cookies, "logined": True
			})
		return res
		return ret

	#tofix
	async def login_username_v11(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via V11 API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/v11/loginregister"
		params = {
			"uname": account["username"],
			"code": account["password"]
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.get(url = url, params = params)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return res
		return ret

	async def login_username_v25(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via V25 API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://v25.chaoxing.com/login"
		data = {"name": account["username"], "pwd": account["password"]}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.post(url = url, data = data)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return ret

	async def login_username_mylogin1(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via Mylogin1 API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/mylogin1"
		data = {
			"fid": "undefined", "msg": account["username"], 
			"vercode": account["password"], "type": 1
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.post(url = url, data = data)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return ret

	async def login_username_xxk(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via XXK API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "http://xxk.chaoxing.com/api/front/user/login"
		params = {
			"username": account["username"],
			"password": account["password"], "numcode": 0
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.get(url = url, params = params)
		if res and res.status == 500 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return ret

	async def login_username_fanya(
		self, account: dict = {"username": "", "password": ""}
	):
		"""Log into Chaoxing account with username and password \
		via Fanya API.
		:param account: Same as ``login_username_v2()``.
		:return: Same as ``login_username_v3()``.
		"""
		url = "https://passport2.chaoxing.com/fanyalogin"
		data = {
			"uname": _encrypt_aes(
				msg = account["username"],
				key = b"u2oh6Vu^HWe4_AES",
				iv = b"u2oh6Vu^HWe4_AES"
			), "password": _encrypt_aes(
				msg = account["password"],
				key = b"u2oh6Vu^HWe4_AES",
				iv = b"u2oh6Vu^HWe4_AES"
			), "t": True
		}
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.post(url = url, data = data)
		if res and res.status == 200 and "p_auth_token" in res.cookies:
			ret.update({"cookies": res.cookies, "logined": True})
		return ret

	async def login_cookies(self, account: dict = {"cookies": None}):
		"""Log into Chaoxing account with cookies.
		:param account: Cookies in dictionary.
		:return: Same as ``login_username_v2()``.
		"""
		url = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
		ret = {"name": "", "cookies": None, "logined": False}
		res = await self.__session.get(
			url = url, cookies = account["cookies"]
		)
		if res and res.status == 200:
			data = await res.json(content_type = None)
			if data["result"]:
				ret.update({
					"name": data["msg"]["name"],
					"cookies": account["cookies"],
					"logined": True
				})
		return ret

	async def curriculum_get_curriculum(self, week: str = ""):
		"""Get curriculum.
		:param week: Week number. Defaulted to the current week.
		:return: Dictionary of curriculum details and lessons \
		containing course IDs, names, classroom locations, teachers \
		and time.
		"""
		def _add_lesson(lesson):
			class_id = str(lesson["classId"])
			lesson = {
				"class_id": class_id,
				"course_id": str(lesson["courseId"]),
				"name": lesson["name"],
				"locations": [lesson["location"]],
				"invite_code": lesson["meetCode"],
				"teachers": [lesson["teacherName"]],
				"times": [{
					"day": str(lesson["dayOfWeek"]),
					"period_begin":
					str(lesson["beginNumber"]),
					"period_end": str(
						lesson["beginNumber"] +
						lesson["length"] - 1
					)
				}]
			}
			if not class_id in curriculum["lessons"]:
				curriculum["lessons"][class_id] = lesson
				return
			_lesson = curriculum["lessons"][class_id]
			if not lesson["locations"][0] in _lesson["locations"]:
				_lesson["locations"].append(
					lesson["locations"][0]
				)
			if not lesson["teachers"][0] in _lesson["teachers"]:
				_lesson["teachers"].append(
					lesson["teachers"][0]
				)
			if not lesson["times"][0] in _lesson["times"]:
				_lesson["times"].append(lesson["times"][0])
		url = "https://kb.chaoxing.com/curriculum/getMyLessons"
		params = {
			"week": week
		}
		res = await self.__session.get(
			url = url, params = params, ttl = 86400
		)
		data = (await res.json()).get("data")
		details = data["curriculum"]
		curriculum = {
			"details": {
				"year": str(details["schoolYear"]),
				"semester": str(details["semester"]),
				"week": str(details["currentWeek"]),
				"week_real": str(details["realCurrentWeek"]),
				"week_max": str(details["maxWeek"]),
				"time": {
					"period_max": str(details["maxLength"]),
					"timetable":
					details["lessonTimeConfigArray"][1 : -1]
				}
			}, "lessons": {}
		}
		lessons = data.get("lessonArray") or []
		for lesson in lessons:
			_add_lesson(lesson = lesson)
			for conflict in lesson.get("conflictLessons") or {}:
				_add_lesson(lesson = conflict)
		return curriculum

	async def course_get_courses(self):
		"""Get all courses in the root folder.
		:return: Dictionary of class IDs to course containing \
		course IDs, names, teachers, status, start and end time.
		"""
		url = "https://mooc2-ans.chaoxing.com/visit/courselistdata"
		params = {"courseType": 1}
		res = await self.__session.get(
			url = url, params = params, ttl = 86400
		)
		active, ended = (await res.text()).split("isState")
		reg = r"Client\('(\d+)','(.*?)','(\d+).*?color3\" " \
		r"title=\"(.*?)\".*?\n(?:[^\n]*?(\d+-\d+-\d+)～(\d+-\d+-\d+))?"
		matches_active = _findall(reg, active, _DOTALL)
		matches_ended = _findall(reg, ended, _DOTALL)
		courses = {}
		def _fill_courses(matches, status):
			for match in matches:
				courses[match[2]] = {
					"class_id": match[2],
					"course_id": match[0],
					"name": match[1],
					"teachers":
					_split(r", |,|，|、", match[3]),
					"status": status,
					"time_start": match[4],
					"time_end": match[5]
				}
		_fill_courses(matches_active, 1)
		_fill_courses(matches_ended, 0)
		return courses

	async def course_get_course_id(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get course ID of a course.
		:param course: Course ID (optional) and clsss ID.
		:return: Course ID corresponding to the class ID.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/class/getClassDetail"
		params = {
			"fid": self.fid, "courseId": "",
			"classId": course["class_id"]
		}
		course_id = course.get("course_id") or \
		self.courses.get(course["class_id"], {}).get("course_id")
		if not course_id:
			res = await self.__session.get(
				url = url, params = params, ttl = 86400
			)
			if res:
				data = (await res.json()).get("data")
				if data:
					course_id = str(data.get("courseid"))
		return course_id or "0"

	async def course_get_location_log(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get checkin location history of a course.
		:param course: Course ID (optional) and class ID.
		:return: Dictionary of activity IDs to checkin locations \
		used by the course.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/sign/getLocationLog"
		params = {
			"DB_STRATEGY": "COURSEID", "STRATEGY_PARA": "courseId",
			"courseId":
			await self.course_get_course_id(course = course),
			"classId": course["class_id"]
		}
		res = await self.__session.get(
			url = url, params = params, ttl = 1800
		)
		data = ((await res.json()).get("data") or []) if res else []
		return {
			location["activeid"]: {
				"latitude": location["latitude"],
				"longitude": location["longitude"],
				"address": location["address"],
				"ranged": 1,
				"range": int(location["locationrange"])
			} for location in data
		} if res else {}

	async def course_get_course_activities_v2(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get activities of a course via V2 API.
		:param course: Course ID (optional) and class ID.
		:return: List of ongoing activities with type, name, \
		activity ID, start, end and remaining time.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
		params = {
			"fid": self.fid, "courseId":
			await self.course_get_course_id(course = course),
			"classId": course["class_id"], "showNotStartedActive": 0
		}
		res = await self.__session.get(
			url = url, params = params, ttl = 60
		)
		data = ((
			(await res.json()).get("data") or {}
		).get("activeList") or []) if res else []
		return [
			{
				"active_id": str(activity["id"]),
				"type": activity["otherId"],
				"name": activity["nameOne"],
				"time_start":
				_strftime(activity["startTime"] // 1000),
				"time_end":
				_strftime(activity["endTime"] // 1000)
				if activity["endTime"] else "",
				"time_left": activity["nameFour"]
			} for activity in data if activity["status"] == 1 and \
			activity.get("otherId") in ("2", "4")
		]

	#tofix
	async def course_get_course_activities_ppt(
		self, course: dict = {"course_id": "", "class_id": ""}
	):
		"""Get activities of a course via PPT API.
		:param course: Course ID (optional) and class ID.
		:return: List of ongoing activities with type, name, \
		activity ID, start, end and remaining time.
		"""
		url = "https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist"
		params = {
			"courseId":
			await self.course_get_course_id(course = course),
			"classId": course["class_id"],
			"showNotStartedActive": 0
		}
		res = await self.__session.get(
			url = url, params = params, ttl = 60
		)
		if not res:
			return []
		data = (await res.json(content_type = None)).get("activeList") or []
		all_details = {}
		_sem = _Semaphore(
			self.config["chaoxing_course_get_activities_workers"]
		)
		async def _get_details(activity):
			async with _sem:
				all_details[activity["active_id"]] = \
				await self.checkin_get_details(
					activity = activity
				)
		await _gather(*[
			_get_details({"active_id": str(activity["id"])})
			for activity in data if not activity["status"] == 1 or
			not activity["activeType"] == 2
		])
		activities = []
		for activity in data:
			if not activity["status"] == 1 or \
			not activity["activeType"] == 2:
				continue
			details = all_details[activity["active_id"]]
			if not details["otherId"] in (2, 4):
				continue
			activities.append({
				"active_id": str(activity["id"]),
				"name": activity["nameOne"],
				"time_start":
				_strftime(activity["startTime"] // 1000),
				"time_left": activity["nameFour"],
				"type": str(details["otherId"]),
				"time_end": _strftime(
					details["endTime"]["time"] // 1000
				) if details["endTime"] else ""
			})
		return activities

	async def course_get_activities(self):
		"""Get activities of all courses.
		:return: Dictionary of Class IDs to ongoing activities.
		"""
		courses = tuple(
			self.courses.values()
		)[: self.config["chaoxing_course_get_activities_courses_limit"]]
		activities = {}
		_sem = _Semaphore(
			self.config["chaoxing_course_get_activities_workers"]
		)
		async def _worker(func, course):
			async with _sem:
				course_activities = await func(course = course)
			if course_activities:
				activities[course["class_id"]] = course_activities
		await _gather(*[_worker(
			self.course_get_course_activities_v2 if i % 2
			else self.course_get_course_activities_ppt, course
		) for i, course in enumerate(courses) if course["status"]])
		return activities

	async def captcha_get_captcha(self, captcha: dict = {"captcha_id": ""}):
		"""Get CAPTCHA for checkin.
		:param captcha: CAPTCHA ID and type.
		:return: CAPTCHA images and token.
		"""
		url1 = "https://captcha.chaoxing.com/captcha/get/conf"
		params1 = {
			"callback": "f", "captchaId": captcha["captcha_id"],
			"_": int(_time() * 1000)
		}
		res1 = await self.__session.get(url = url1, params = params1)
		captcha = {
			**captcha, "type": "slide", "server_time": _search(
				r"t\":(\d+)", await res1.text()
			).group(1)
		}
		captcha_key, token = _generate_secrets(captcha = captcha)
		url2 = "https://captcha.chaoxing.com/captcha/get/verification/image"
		params2 = {
			"callback": "f",
			"captchaId": captcha["captcha_id"],
			"captchaKey": captcha_key,
			"token": token,
			"type": "slide", "version": "1.1.16",
			"referer": "https://mobilelearn.chaoxing.com",
			"_": int(_time() * 1000)
		}
		res2 = await self.__session.get(url = url2, params = params2)
		data2 = _literal_eval((await res2.text())[2 : -1])
		captcha.update({
			"token": data2["token"],
			"big_img_src":
			data2["imageVerificationVo"]["shadeImage"],
			"small_img_src":
			data2["imageVerificationVo"]["cutoutImage"]
		})
		return captcha

	async def captcha_submit_captcha(
		self, captcha = {"captcha_id": "", "token": "", "vcode": ""}
	):
		"""Submit and verify CAPTCHA.
		:param captcha: CAPTCHA ID, and verification code (e.g. slider \
		offset) in dictionary.
		:return: CAPTCHA with validation code on success.
		"""
		url = "https://captcha.chaoxing.com/captcha/check/verification/result"
		params = {
			"callback": "f",
			"captchaId": captcha["captcha_id"],
			"token": captcha["token"],
			"textClickArr": f"[{{\"x\": {captcha['vcode']}}}]",
			"type": "slide", "coordinate": "[]",
			"version": "1.1.16", "runEnv": 10,
			"_": int(_time() * 1000)
		}
		res = await self.__session.get(
			url = url, params = params, headers = {
				**self.__session.headers,
				"Referer": "https://mobilelearn.chaoxing.com"
			}
		)
		return "result\":true" in await res.text() if res else False, {
			**captcha, "validate":
			f"validate_{captcha['captcha_id']}_{captcha['token']}"
		}

	#tofix
	async def checkin_get_details(self, activity: dict = {"active_id": ""}):
		"""Get checkin details.
		:param activity: Activity ID.
		:return: Checkin details including class ID on success.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/signDetail"
		params = {"activePrimaryId": activity["active_id"], "type": 1}
		res = await self.__session.get(
			url = url, params = params, ttl = 300
		)
		try:
			return await res.json(content_type = None) if res else {}
		except Exception as e:
			raise e

	async def checkin_get_pptactiveinfo(
		self, activity: dict = {"active_id": ""}
	):
		"""Get checkin PPT activity information.
		:param activity: Activity ID.
		:return: Checkin PPT activity details including class ID \
		and ranged flag on success.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo"
		params = {"activeId": activity["active_id"]}
		res = await self.__session.get(
			url = url, params = params, ttl = 60
		)
		return (await res.json())["data"] if res else {}

	def checkin_format_location(
		self,
		location: dict = {"latitude": -1, "longitude": -1, "address": ""},
		new_location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Format checkin location.
		:param location: Address, latitude and longitude. \
		Used for address override for checkin location.
		:param location_new: Address, latitude and longitude. \
		The checkin location to upload.
		:return: Checkin location containing address, latitude, \
		longitude, range and ranged flag.
		"""
		new_location = {"ranged": 0, "range": 0, **new_location}
		_rand = lambda x: round(x - 0.0005 + _uniform(0, 0.001), 6)
		if self.config["chaoxing_checkin_location_randomness"]:
			new_location.update({
				"latitude": _rand(new_location["latitude"]),
				"longitude": _rand(new_location["longitude"])
			})
		if len(new_location["address"]) < self.config[
			"chaoxing_checkin_location_address_override_maxlen"
		]:
			new_location["address"] = location["address"]
		return new_location

	async def checkin_get_location(
		self, activity: dict = {"active_id": ""},
		course: dict ={"course_id": "", "class_id": ""}
	):
		"""Get checkin location from the location log of its \
		corresponding course.
		:param activity: Activity ID in dictionary.
		:param course: Course ID (optional) and class ID.
		:return: Checkin location containing address, latitude, \
		longitude, range and ranged flag.
		"""
		locations = await self.course_get_location_log(course = course)
		return locations.get(
			activity["active_id"], next(iter(locations.values()))
		) if locations else {
			"latitude": -1, "longitude": -1, "address": "",
			"ranged": 0, "range": 0
		}

	async def checkin_do_analysis(self, activity: dict = {"active_id": ""}):
		"""Do checkin analysis.
		:param activity: Activity ID in dictionary.
		:return: True on success, otherwise False.
		"""
		url1 = "https://mobilelearn.chaoxing.com/pptSign/analysis"
		params1 = {
			"vs": 1, "DB_STRATEGY": "RANDOM",
			"aid": activity["active_id"]
		}
		res1 = await self.__session.get(
			url = url1, params = params1, ttl = 1800
		)
		if not res1:
			return False
		url2 = "https://mobilelearn.chaoxing.com/pptSign/analysis2"
		params2 = {
			"DB_STRATEGY": "RANDOM", "code":
			_search(r"([0-9a-f]{32})", await res1.text()).group(1)
		}
		res2 = await self.__session.get(
			url = url2, params = params2, ttl = 1800
		)
		return await res2.text() == "success" if res2 else False

	async def checkin_do_presign(
		self, activity: dict = {"active_id": ""},
		course: dict ={"course_id": "", "class_id": ""}
	):
		"""Do checkin pre-sign.
		:param activity: Activity ID in dictionary.
		:param course: Course ID (optional) and class ID.
		:return: Presign state (2 if checked-in or 1 on success), \
		checkin location and CAPTCHA.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/preSign"
		params = {
			"courseId":
			await self.course_get_course_id(course = course),
			"classId": course["class_id"],
			"activePrimaryId": activity["active_id"],
			"general": 1, "sys": 1, "ls": 1, "appType": 15,
			"tid": "", "uid": self.uid, "ut": "s"
		}
		location = {
			"latitude": -1, "longitude": -1, "address": "",
			"ranged": 0, "range": 0
		}
		captcha = {"captcha_id": ""}
		res = await self.__session.get(url = url, params = params)
		if not res or res.status != 200:
			return 0, location, captcha
		state = 1
		match = _search(
			r"ifopenAddress\" value=\"(\d)\"(?:.*?locationText\" "
			r"value=\"(.*?)\".*?locationLatitude\" value="
			r"\"(\d+\.\d+)\".*?locationLongitude\" value="
			r"\"(\d+\.\d+)\".*?locationRange\" value="
			r"\"(\d+))?.*?captchaId: '([0-9A-Za-z]{32})|"
			r"(zsign_success)", await res.text(), _DOTALL
		)
		if match:
			if match.group(7):
				state = 2
			if match.group(1) == "1":
				location = {
					"latitude": float(match.group(3) or -1),
					"longitude":
					float(match.group(4) or -1),
					"address": match.group(2) or "",
					"ranged": int(match.group(1)),
					"range": int(match.group(5) or 0)
				}
			captcha["captcha_id"] = match.group(6)
		return state, location, captcha

	async def checkin_do_sign(
		self, activity: dict = {"active_id": "", "type": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": "", "ranged": 0},
		old_params: dict = {"name": "", "uid": "", "fid": "", "...": "..."}
	):
		"""Do checkin sign.
		:param activity: Activity ID and type in dictionary.
		:param location: Address, latitude, longitude and ranged flag.
		:param old_params: Reuse previous parameters. \
		Overrides activity and location if given.
		:return: Sign state (True on success), message and parameters.
		"""
		url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax"
		if old_params.get("activeId"):
			params = old_params
		else:
			params = {
				"name": "",
				"uid": self.uid, "fid": self.fid,
				"activeId": activity["active_id"],
				"enc": activity.get("enc", ""),
				"enc2": "", "address": "", "latitude": -1,
				"longitude": -1, "location": "", "ifTiJiao": 0,
				"appType": 15, "clientip": "", "validate": ""
			}
			if activity["type"] == "4":
				params.update({
					"address": location["address"],
					"latitude": location["latitude"],
					"longitude": location["longitude"],
					"ifTiJiao": location["ranged"]
				})
			elif activity["type"] == "2":
				params.update({
					"location": str(location),
					"ifTiJiao": location["ranged"]
				} if location["ranged"] else {
					"address": location["address"],
					"latitude": location["latitude"],
					"longitude": location["longitude"]
				})
		status = False
		res = await self.__session.get(url = url, params = params)
		text = await res.text()
		if text in ("success", "您已签到过了"):
			status = True
			msg = f"Checkin success. ({text})"
		else:
			match = _search(r"validate_([0-9A-Fa-f]{32})", text)
			if match:
				params["enc2"] = match.group(1)
			msg = f"Checkin failure. {text}"
		return status, {"msg": msg, "params": params}

	async def checkin_checkin_location(
		self, activity: dict = {"active_id": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Location checkin.
		:param activity: Activity ID in dictionary.
		:param location: Address, latitude and longitude. \
		Overriden by server-side location if any.
		:return: Checkin state (True on success), message, \
		parameters and captcha (``{}`` if checked-in or failed).
		"""
		try:
			_analyze = _create_task(self.checkin_do_analysis(
				activity = activity
			))
			info = await self.checkin_get_details(
				activity = activity
			)
			assert info["status"] == 1 and not info["isDelete"], \
			"Activity ended or deleted."
			course = {"class_id": str(info["clazzId"])}
			presign = await self.checkin_do_presign(
				activity = activity, course = course
			)
			assert presign[0], \
			f"Presign failure. {activity, presign}"
			if presign[0] == 2:
				return True, {
					"msg":
					"Checkin success. (Already checked in.)",
					"params": "", "captcha": ""
				}
			location = self.checkin_format_location(
				location = location, new_location = presign[1]
			) if presign[1]["ranged"] else {**location, "ranged": 0}
			await _analyze
			result = await self.checkin_do_sign(
				activity = {**activity, "type": "4"},
				location = location
			)
			result[1]["captcha"] = presign[2]
			return result
		except Exception as e:
			return False, {
				"msg": str(e), "params": {}, "captcha": {}
			}

	async def checkin_checkin_qrcode(
		self, activity: dict = {"active_id": "", "enc": ""},
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Qrcode checkin.
		:param activity: Activity ID and ENC in dictionary.
		:param location: Same as ``checkin_checkin_location()``.
		:return: Same as ``checkin_checkin_location()``.
		"""
		try:
			_analyze = _create_task(self.checkin_do_analysis(
				activity = activity
			))
			info = self.checkin_get_details(activity = activity)
			assert info["status"] == 1 and not info["isDelete"], \
			"Activity ended or deleted."
			course = {"class_id": str(info["clazzId"])}
			_locate = _create_task(self.checkin_format_location(
				location = location,
				new_location = await self.checkin_get_location(
					activity = activity, course = course
				)
			))
			presign = await self.checkin_do_presign(
				activity = activity, course = course
			)
			assert presign[0], f"Presign failure. {activity, presign}"
			if presign[0] == 2:
				return True, {
					"msg":
					"Checkin success. (Already checked in.)",
					"params": "", "captcha": ""
				}
			if presign[1]["ranged"]:
				location = self.checkin_format_location(
					location = location,
					new_location = await _locate
				)
			else:
				location["ranged"] = 0
			await _analyze
			result = await self.checkin_do_sign(
				activity = {**activity, "type": "2"},
				location = location
			)
			result[1]["captcha"] = presign[2]
			return result
		except Exception as e:
			return False, {
				"msg": str(e), "params": {}, "captcha": {}
			}

	async def checkin_checkin_qrcode_url(
		self, url: str = "",
		location: dict = {"latitude": -1, "longitude": -1, "address": ""}
	):
		"""Qrcode checkin.
		:param url: URL from Qrcode.
		:param location: Same as ``checkin_checkin_location()``.
		:return: Same as ``checkin_checkin_location()``.
		"""
		try:
			assert "mobilelearn.chaoxing.com/widget/sign/e" \
			in url, f"Checkin failure. {'Invalid URL.', url}"
			match = _search(r"id=(\d+).*?([0-9A-F]{32})", url)
			return await self.checkin_checkin_qrcode(activity = {
				"active_id": match.group(1),
				"enc": match.group(2)
			}, location = location)
		except Exception as e:
			return False, {
				"msg": str(e), "params": {}, "captcha": {}
			}
