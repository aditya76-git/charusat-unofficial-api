import requests
import json
from urllib.parse import urlencode
from .errors import MissingCredentialsError
from .utils import parse_attendance_html, extract_payload_values, parse_attendance_status_html, parse_fees_data, parse_result_data, extract_payload_values_for_results, parse_previous_exam_details, parse_user_info
from .private_api import CharusatPrivateAPI


class CharusatScraper:
    '''
    Unofficial scraper for accessing student information from Charusat University's website.

    This class provides methods to interact with the university's website, retrieve
    student details, attendance, timetable, fees, and more.

    Methods:
        setup: Initialize headers and session for making requests.
        setup_login_cookie_values: Extract and set login cookies.
        check_credentials: Check if username and password are provided.
        get_user_details: Retrieve and return user details.
        get_attendance: Retrieve and return attendance data.
        get_timetable: Retrieve and return the student's timetable.
        get_fees_details: Retrieve and return fee details.
        get_result_data: Retrieve and return result data. (pending...)
    '''

    def __init__(self, username, password):
        self.BASE_URL = "https://charusat.edu.in:912"
        self.username = username
        self.password = password
        self.check_credentials()
        self.session = requests.Session()
        self.setup()
        self.setup_login_cookie_values()

    def check_credentials(self):
        '''
        Check if both username and password are provided.

        Raises:
            MissingCredentialsError: If either the username or password is missing.

        Returns:
            bool: True if both username and password are provided.
        '''
        if not self.username or not self.password:
            raise MissingCredentialsError("One or Other Credentail Missing")
        return True

    def setup(self):
        '''
        Set up the necessary headers and login payload values for making requests.

        This method initializes the required headers for sending HTTP requests and obtains the login payload values needed for authentication.

        This method is called once during the initialization of the
        CharusatScraper class.
        '''
        self.login_payload_values = self.get_payload_values("/eGovernance/")
        self.HEADERS = {
            "authority": "charusat.edu.in:912",
            "accept": "*/*",
            "accept-language": "en",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://charusat.edu.in:912",
            "referer": "https://charusat.edu.in:912/eGovernance/",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "x-microsoftajax": "Delta=true",
        }
        self.session.headers.update(self.HEADERS)

    def get_payload_values(self, path):
        html_data = self.session.get("{}{}".format(self.BASE_URL, path)).text
        result = extract_payload_values(html_data)
        return result

    def extract_cookies(self):
        '''
        Extract and return cookies from the HTTP response after login.

        After successful login, the method expects two important cookies:
            - ASP.NET_SessionId: Used for session management.
            - .EGovWebApp: Contains session information for subsequent requests.
        '''
        form_data = {
            "ScriptManager1": "up1|btnLogin",
            "__EVENTTARGET": "btnLogin",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": self.login_payload_values.get("__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": self.login_payload_values.get(
                "__VIEWSTATEGENERATOR"
            ),
            "__EVENTVALIDATION": self.login_payload_values.get("__EVENTVALIDATION"),
            "txtUserName": self.username,
            "txtPassword": str(self.password),
            "hdnGPLevel": "",
            "txtUserID": "",
            "txtName": "",
            "hdnPassword": "",
            "txtAccountType": "",
            "txtEmail": "",
            "hdnPasswordFlg": "-1",
            "hdnAuthorizedPerson": "",
            "hdnUserType": "",
            "__ASYNCPOST": "true",
        }

        encoded_data = urlencode(form_data)

        response = self.session.post(
            "{}/eGovernance/Home.aspx".format(self.BASE_URL),
            headers=self.HEADERS,
            data=encoded_data,
        )

        cookie_dict = {
            cookie.name: cookie.value for cookie in response.cookies
        }

        return cookie_dict

    def setup_login_cookie_values(self):
        '''
        Set up essential cookies after a successful login.
        '''
        cookie_dict = self.extract_cookies()
        if ".EGovWebApp" in cookie_dict and "ASP.NET_SessionId" in cookie_dict:
            self.EGOV_WEB_APP_COOKIE = cookie_dict[".EGovWebApp"]
            self.ASP_NET_SESSIONID_COOKIE = cookie_dict["ASP.NET_SessionId"]
        else:
            raise ValueError(
                "Check Login Details. Both '.EGovWebApp' and 'ASP.NET_SessionId' cookies are required in the dictionary."
            )

    def get_attendance(self):
        '''
        Retrieve HTML data containing Gross Lecture Attendance information for the authenticated user and return it after parsing the data.
        '''

        payload_values = self.get_payload_values(
            "/eGovernance/frmAppSelection.aspx")

        data = {
            "ScriptManager1": "UpGrossAtt|grdGrossAtt$ctl01$lnkRequestViewTT",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": payload_values.get("__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": payload_values.get("__VIEWSTATEGENERATOR"),
            "__EVENTVALIDATION": payload_values.get("__EVENTVALIDATION"),
            "__ASYNCPOST": "true",
            "grdGrossAtt$ctl01$lnkRequestViewTT.x": "242",
            "grdGrossAtt$ctl01$lnkRequestViewTT.y": "80",
        }

        response = self.session.post(
            "{}/eGovernance/frmAppSelection.aspx".format(self.BASE_URL),
            data=data,
        )

        return parse_attendance_html(response.text)

    def get_attendance_status_web(self):
        '''
        Retrieve HTML data containing Attendance information for the authenticated user and return it after parsing the data.

        Note:
            - At present, it is only possible to retrieve lecture attendance data for the most recent day.
        '''

        payload_values = self.get_payload_values(
            "/eGovernance/frmAppSelection.aspx")

        data = {
            'ScriptManager1': 'upTimeTable|gvTimetable_stu$ctl01$lnkRequestViewTT',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            "__VIEWSTATE": payload_values.get("__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": payload_values.get("__VIEWSTATEGENERATOR"),
            "__EVENTVALIDATION": payload_values.get("__EVENTVALIDATION"),
            '__ASYNCPOST': 'true',
            'gvTimetable_stu$ctl01$lnkRequestViewTT.x': '236',
            'gvTimetable_stu$ctl01$lnkRequestViewTT.y': '117',
        }

        response = self.session.post(
            "{}/eGovernance/frmAppSelection.aspx".format(self.BASE_URL),
            data=data,
        )

        return parse_attendance_status_html(response.text)

    def get_attendance_status(self, date=None):

        privateAPI = CharusatPrivateAPI(self.username, self.password)

        return privateAPI.get_attendance_status(date=date)

    def get_fees_details(self):
        '''
        Retrieve HTML data containing Fees information for the authenticated user and return it after parsing the data.
        '''

        payload_values = self.get_payload_values(
            "/eGovernance/frmAppSelection.aspx")

        data = {
            'ScriptManager1': 'upPendingAtt|gvfees$ctl01$lnkgvFees',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ddlsemester',
            '__LASTFOCUS': '',
            '__VIEWSTATE': payload_values.get("__VIEWSTATE"),
            '__VIEWSTATEGENERATOR': payload_values.get("__VIEWSTATEGENERATOR"),
            '__EVENTVALIDATION': payload_values.get("__EVENTVALIDATION"),
            '__ASYNCPOST': 'true',
            'gvfees$ctl01$lnkgvFees.x': '281',
            'gvfees$ctl01$lnkgvFees.y': '127',
        }

        response = self.session.post(
            "{}/eGovernance/frmAppSelection.aspx".format(self.BASE_URL),
            data=data,
        )

        return parse_fees_data(response.text)

    def get_results_payload(self):

        payload_values = self.get_payload_values(
            "/eGovernance/frmAppSelection.aspx")

        data = {
            'ScriptManager1': 'updSchedule|gvresult1$ctl01$lnkRequestViewTT',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': payload_values.get("__VIEWSTATE"),
            '__VIEWSTATEGENERATOR': payload_values.get("__VIEWSTATEGENERATOR"),
            '__EVENTVALIDATION': payload_values.get("__EVENTVALIDATION"),
            '__ASYNCPOST': 'true',
            'gvresult1$ctl01$lnkRequestViewTT.x': '262',
            'gvresult1$ctl01$lnkRequestViewTT.y': '122',
        }

        response = self.session.post(
            "{}/eGovernance/frmAppSelection.aspx".format(self.BASE_URL),
            data=data,
        )

        result = extract_payload_values_for_results(response.text)

        return result

    def get_result_data_web(self, sem=1):
        '''
        Retrieve result data for a specified semester. However, please be aware of the current limitations:

        - The inclusion of __VIEWSTATE, __VIEWSTATEGENERATOR, and __EVENTVALIDATION in the payload is currently ineffective, rendering this method non-functional at the moment.

        - The method 'get_results_payload' has been created, but it does not facilitate authentication with the frmAppSelection.aspx route to retrieve result data.

        - Obtaining values from the Developer Tools can sometimes make this method partially functional, although it is not consistently reliable.

        These limitations are actively being addressed, and the method will be updated once the issues are resolved.
        '''

        payload_values = self.get_results_payload()

        data = {
            'ScriptManager1': 'updSchedule|ddlsemester',
            'txtdate': '15/09/2023',
            'meeDate_ClientState': '',
            'ddlsemester': "2",
            '__EVENTTARGET': 'ddlsemester',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': payload_values.get("VIEWSTATE"),
            '__VIEWSTATEGENERATOR': payload_values.get("VIEWSTATEGENERATOR"),
            '__EVENTVALIDATION': payload_values.get("EVENTVALIDATION"),
            '__ASYNCPOST': 'true',
            '': ''
        }

        response = self.session.post(
            "{}/eGovernance/frmAppSelection.aspx".format(self.BASE_URL),
            data=data,
        )

        print(response.text)

        return parse_result_data(response.text)

    def get_result_data(self, sem=1, month_year=None):
        '''
        Retrieve result data for a specific semester using the APP API, offering a more efficient and faster alternative to web scraping. 

        The APP API requires a less payload compared to the web login method
        '''
        privateAPI = CharusatPrivateAPI(self.username, self.password)

        return privateAPI.get_result_data(sem=sem, month_year=month_year)

    def get_user_details(self):
        '''
        Retrieve HTML data containing User information and Previous Exam Details for the authenticated user and return it after parsing the data.
        '''
        response = self.session.post(
            "{}/eGovernance/SES/frmEnrollment.aspx".format(self.BASE_URL))

        user_info = parse_user_info(response.text)
        previous_exam_details = parse_previous_exam_details(response.text)

        data = {
            "user_info": user_info,
            "previous_exam_details": previous_exam_details
        }

        return json.dumps(data, indent=4)
