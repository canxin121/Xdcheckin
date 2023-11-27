# -*- coding: utf-8 -*-

from re import findall, search
import requests
from urllib.parse import parse_qs, unquote, urlparse

class Chaoxing:
	name = uid = cookies = courses = logined = None
	headers = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
	}

	def __init__(self, username: str = "", password: str = "") -> None:
		requests.packages.urllib3.disable_warnings()
		try:
			assert username
			assert password
			login = self.login(account = {"username": username, "password": password})
			self.name, self.uid, self.cookies = login["name"], login["uid"], login["cookies"]
			self.courses = self.get_courses()
			assert self.courses
			self.logined = (login != False)
		except Exception:
			self.logined = False

	def get(self, url, params: dict = {}, cookies: requests.cookies.RequestsCookieJar = None, headers: dict = None, verify = False):
		cookies = cookies if cookies else self.cookies
		headers = headers if headers else self.headers
		return requests.get(url, params = params, cookies = cookies, headers = headers, verify = False)

	def login(self, account: dict = {"username": "", "password": ""}) -> dict | bool:
		"""Log into Chaoxing account.
		:param account: Username and password in dictionary.
		:return: Name, UID and cookies on success, otherwise False.
		"""
		url1 = "https://passport2-api.chaoxing.com/v11/loginregister"
		params1 = {
			"code": account["password"],
			"cx_xxt_passport": "json",
			"uname": account["username"],
			"loginType": 1,
			"roleSelect": "true"
		}
		url2 = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
		try:
			res1 = self.get(url1, params1)
			assert res1.json()["status"]
			res2 = self.get(url2, cookies = res1.cookies)
			data = res2.json()
			assert data["result"]
			return {
				"name": str(data["msg"]["name"]),
				"uid": str(data["msg"]["puid"]),
				"cookies": res1.cookies
			}
		except Exception:
			return False

	def get_courses(self) -> dict | bool:
		"""Get course IDs corresponding to class IDs.
		:return: Dictionary of class IDs to course IDs on success, otherwise False.
		"""
		url = "https://mooc1-1.chaoxing.com/visit/courselistdata"
		params = {
			"courseType": 1,
			"courseFolderId": 0,
			"courseFolderSize": 0
		}
		try:
			res = self.get(url, params)
			courses = findall(r"<.*courseId=\"(.*?)\" clazzId=\"(.*?)\" .*>", res.text)
			return {row[1]: row[0] for row in courses}
		except Exception:
			return False

	def get_course_activities(self, course: dict = {"course_id": "", "class_id": ""}) -> list[dict] | bool:
		"""Get activities of a course.
		:param course: Course ID (unnecessary) and class ID in dictionary.
		:return: List of dictionaries of ongoing activities with type, name, activity ID and remaining time on success, otherwise False.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
		params = {
			"fid": 0,
			"courseId": course["course_id"] if course["course_id"] else self.courses[course["class_id"]],
			"classId": course["class_id"],
			"showNotStartedActive": 0
		}
		try:
			res = self.get(url, params)
			data = res.json()["data"]["activeList"]
			activities = [{"active_id": activity["id"], "type": activity["otherId"], "time_left": activity["nameFour"]} for activity in data if activity["otherId"] in ("2", "4") and activity["status"] == 1]
			assert activities
			return activities
		except Exception:
			return False

	def get_activities(self) -> list[dict] | bool:
		"""Get activities of all courses.
		:param course: Course ID (unnecessary) and class ID in dictionary.
		:return: Dictionary of class IDs to ongoing activities if any, otherwise False.
		"""
		try:
			activities = {}
			for class_id, course_id in self.courses.items():
				activity = self.get_course_activities({"course_id": course_id, "class_id": class_id})
				if activity:
					activities[class_id] = activity
			assert activities
			return activities
		except Exception:
			return False

	def location_to_string(self, location: dict = {"latitude": -1, "longitude": -1, "address": ""}) -> str:
		"""Convert location dictionary to string.
		:param location: Address, latitude and longitude in dictionary.
		:return: Location string.
		"""
		return "{\"result\":1,\"latitude\":" + str(location["latitude"]) + ",\"longitude\":" + str(location["longitude"]) + ",\"address\":\"" + location["address"] + "\"}"

	def checkin_get_details(self, activity: dict = {"active_id": ""}) -> dict | bool:
		"""Get checkin details
		:param activity: Activity ID in dictionary.
		:return: Checkin details including class ID and MSG code on success, otherwise False.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/signDetail"
		params = {
			"activePrimaryId": activity["active_id"],
			"type": "1"
		}
		try:
			res = self.get(url, params)
			details = res.json().items()
			assert len(details)
			return {key: str(val) if val is not None else "" for key, val in details}
		except Exception:
			return False

	def checkin_do_presign(self, activity: dict = {"active_id": "", "class_id": ""}) -> str:
		"""Do checkin pre-sign.
		:param active_id: Activity ID and Class ID in dictionary.
		:return: Returns True on success, otherwise False.
		"""
		url = "https://mobilelearn.chaoxing.com/newsign/preSign"
		params = {
			"courseId": self.courses.get(activity["class_id"]) or "",
			"classId": activity["class_id"],
			"activePrimaryId": activity["active_id"],
			"general": "1",
			"sys": "1",
			"ls": "1",
			"appType": "15",
			"tid": "",
			"uid": self.uid,
			"ut": "s"
		}
		try:
			res = self.get(url, params)
			return res.status_code == 200
		except Exception:
			return False

	def checkin_do_analysis(self, activity: dict = {"active_id": ""}) -> bool:
		"""Do checkin analysis.
		:param activity: Activity ID in dictionary.
		:return: Returns True on success, otherwise False.
		"""
		url1 = "https://mobilelearn.chaoxing.com/pptSign/analysis"
		params1 = {
			"vs": "1",
			"DB_STRATEGY": "RANDOM",
			"aid": activity["active_id"]
		}
		url2 = "https://mobilelearn.chaoxing.com/pptSign/analysis2"
		params2 = {
			"DB_STRATEGY": "RANDOM",
			"code": ""
		}
		try:
			res1 = self.get(url1, params1)
			params2["code"] = search(r"code=\'\+\'(.*?)\'", res1.text).group(1)
			res2 = self.get(url2, params2)
			return res2.text == "success"
		except Exception:
			return False

	def checkin_check_designatedplace(self, activity: dict = {"active_id": ""}) -> bool:
		"""Check if designated location is enabled. Defaults to True. Must be called for all checkin types.
		:param activity: Activity ID in dictionary.
		"""
		url = "https://mobilelearn.chaoxing.com/v2/apis/active/getPPTActiveInfo"
		params = {
			"activeId": activity["active_id"]
		}
		try:
			res = self.get(url, params)
			s = search(r"\"locationRange\":(.*?),", res.text)
			return s.group(1) != "null"
		except Exception:
			return True

	def checkin_checkin_location(self, activity: dict = {"active_id": ""}, location: dict = {"latitude": -1, "longitude": -1, "address": ""}) -> bool:
		"""Location checkin.
		:param active_id: Activity ID in dictionary.
		:param location: Address, latitude and longitude in dictionary. Unused if designated place not enabled.
		:return: Returns True on success, otherwise False.
		"""
		sign_details = self.checkin_get_details(activity = activity)
		activity["class_id"] = sign_details["clazzId"]
		assert self.checkin_do_presign(activity = activity)
		assert self.checkin_do_analysis(activity = activity)
		ranged = + self.checkin_check_designatedplace(activity = activity)
		url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax"
		params = {
			"address": location["address"] if ranged else "",
			"activeId": activity["active_id"],
			"latitude": location["latitude"] if ranged else -1,
			"longitude": location["longitude"] if ranged else -1,
			"fid": 0,
			"appType": 15,
			"ifTiJiao": ranged
		}
		try:
			res = self.get(url, params)
			return res.text in ("success", "您已签到过了")
		except Exception:
			return False

	def checkin_checkin_qrcode(self, activity: dict = {"active_id": "", "enc": ""}, location: dict = {"latitude": -1, "longitude": -1, "address": ""}) -> bool:
		"""Qrcode checkin.
		:param active_id: Activity ID and ENC code in dictionary.
		:param location: Address, latitude and longitude in dictionary. Unused if designated place not enabled.
		:return: Returns True on success, otherwise False.
		"""
		sign_details = self.checkin_get_details(activity = activity)
		activity["class_id"] = sign_details["clazzId"]
		assert self.checkin_do_presign(activity = activity)
		assert self.checkin_do_analysis(activity = activity)
		ranged = + self.checkin_check_designatedplace(activity = activity)
		url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax"
		params = {
			"enc": activity["enc"],
			"activeId": activity["active_id"],
			"location": self.location_to_string(location) if ranged else "",
			"latitude": -1 if ranged else location["latitude"],
			"longitude": -1 if ranged else location["longitude"],
			"fid": 0
		}
		try:
			res = self.get(url, params)
			return res.text in ("success", "您已签到过了")
		except Exception:
			return False

	def checkin_checkin_qrcode_url(self, qr_url: str = "", location: dict = {"latitude": -1, "longitude": -1, "address": ""}) -> bool:
		"""Qrcode checkin.
		:param qr_url: URL from qrcode.
		:param location: Address, latitude and longitude in dictionary. Unused if designated place not enabled.
		:return: Returns True on success, otherwise False.
		"""
		if qr_url.find("https://mobilelearn.chaoxing.com/widget/sign/e"):
			return False
		params = parse_qs(urlparse(unquote(qr_url)).query)
		try:
			activity = {
				"active_id": params["id"][0],
				"enc": params["enc"][0]
			}
			return self.checkin_checkin_qrcode(activity = activity, location = location)
		except Exception:
			return False
