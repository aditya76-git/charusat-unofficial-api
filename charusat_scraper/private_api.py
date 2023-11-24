import requests
import json
import datetime


class CharusatPrivateAPI:
    '''
    The class uses APP API to retrieve Data which is more convienient and faster than the WEB Method.
    Only Lecture Gross Attendance is not shown in APP rest everything works fine with the APP
    '''

    def __init__(self, username, password):
        '''
        Initialize the CharusatPrivateAPI instance with the provided username and password.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.'''
        self.BASE_URL = "http://117.239.83.200:911"
        self.HEADERS = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/4.5.0"
        }
        # Constant EPara1 payload value for each Request
        self.E_PARA1 = "cCavZvyIrpoUEvBaP896+Q=="
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.setup_studentsysid()

    def setup_studentsysid(self):
        self.studentsysid = self.get_student_info().get("studentsysid", None)

    def get_student_info(self):
        '''
        Get student information using the APP API.

        Returns:
            dict: A dictionary containing student information.

        Raises:
            Exception: If there's an error decoding the JSON response.

        '''
        payload = {
            "EPara1": self.E_PARA1,
            "EPara2": self.username,
            "EPara3": str(self.password),
            "EPara4": ""
        }

        response = self.session.post(
            "{}/api/Water/eMethod219".format(self.BASE_URL), data=json.dumps(payload))

        try:
            response = response.json()
            if response['UserDetails'][0]['Message'] == "Success":
                return response['UserDetails'][0]
        except:
            raise Exception("Error decoding JSON Response")

    def get_schedule_exam_id(self, sem=1, month_year=None):
        """
        Get the schedule exam ID for a specific semester and month_year using the APP API.

        Args:
            semester (int): The target semester for which you want to retrieve the schedule exam ID.
            month_year (str): The month and year (e.g., "April 2023" or "APRIL 2023" or "april 2023") for which you want to retrieve the schedule exam ID.

        Returns:
            int: The ScheduleExamID for the specified semester or month_year.

        Raises:
            Exception: If there's an error finding studentsysid or decoding the JSON response.
        """

        if month_year is not None:

            month_year = month_year.split(" ")  # APRIL 2023

            # Works even If User Requested with month in lowercase

            year = month_year[-1]
            month = month_year[0].upper()
            month_year = f"{month} {year}"

        studentsysid = self.studentsysid

        if studentsysid is None:
            raise Exception("Error Finding studentsysid")

        payload = {
            "EPara1": self.E_PARA1,
            "EPara2": str(studentsysid),  # studentsysid
            "EPara3": str(sem),  # sem,
            "EPara4": "M",
            "EPara5": self.password
        }

        response = self.session.post(
            "{}/api/Water/eMethod683".format(self.BASE_URL), data=json.dumps(payload))

        try:
            response = response.json()
            tblScheduleExam = response['tblScheduleExam']

            if month_year is not None:
                for exam in tblScheduleExam:
                    if exam['ExamMonthYear'] == month_year:
                        ScheduleExamID = exam.get('ScheduleExamID')
                        break
            else:
                # defaults to the Latest exam
                ScheduleExamID = tblScheduleExam[0].get("ScheduleExamID")

            return ScheduleExamID

        except:
            raise Exception("Error Decoding JSON Response")

    def get_result_data(self, sem=1, month_year=None):
        '''
        Get result data for a specific semester or month_year using the APP API.

        Args:
            semester (int): The target semester for which you want to retrieve result data.
            month_year (str): The month and year (e.g., "April 2023") for which you want to retrieve result data.

        Returns:
            str: A JSON string containing the result data.

        Raises:
            Exception: If there's an error decoding the JSON response.
        '''
        studentsysid = self.studentsysid

        ScheduleExamID = self.get_schedule_exam_id(
            sem=sem, month_year=month_year)

        payload = {
            "EPara1": self.E_PARA1,
            "EPara2": str(studentsysid),  # studentsysid
            "EPara3": str(ScheduleExamID),  # ScheduleExamID,
            "EPara4": "M",
            "EPara5": str(self.password)
        }
        response = requests.post(
            f"{self.BASE_URL}/api/Water/eMethod467", data=json.dumps(payload))

        try:
            response = response.json()

            result_data = {
                'result': [],
                'summary': []}

            for res in response.get('tblStudentResultDet', []):
                course_data = {
                    'courseName': res.get("SubjectName", ""),
                    'courseCode': res.get("SubjectCode", ""),
                    'padagoggy': res.get("Padagoggy", ""),
                    'credit': res.get("Credit", ""),
                    'grade': res.get("Grade", ""),
                    'parentSubjectID': res.get("ParentSubjectID", "")
                }
                result_data['result'].append(course_data)

            tblStudentResultMst = response.get('tblStudentResultMst', [])[0]

            summary_data = {
                "studentName": tblStudentResultMst.get("StudentName", ""),
                "studentID": tblStudentResultMst.get("StudentID", ""),
                "facultyName": tblStudentResultMst.get("FacultyName", ""),
                "date": tblStudentResultMst.get("Date", ""),
                "program": tblStudentResultMst.get("Program", ""),
                "examMonthYear": tblStudentResultMst.get("ExamMonthYear", ""),
                "studentType": tblStudentResultMst.get("StudentType", ""),
                "totalCredits": tblStudentResultMst.get("totCredit", ""),
                "creditEarned": tblStudentResultMst.get("CreditEarned", ""),
                "creditEarned": tblStudentResultMst.get("CreditEarned", ""),
                "sgpa": tblStudentResultMst.get("sgpa", ""),
                "cgpa": tblStudentResultMst.get("cgpa", ""),
                "noofbacklog": tblStudentResultMst.get("noofbacklog", ""),
                "studentLastSem": tblStudentResultMst.get("StudentLastSem", ""),
            }

            result_data['summary'].append(summary_data)

            return result_data

        except:
            raise Exception(
                "Error Decoding JSON Response")

    def get_attendance_status(self, date=None):
        '''
        Get attendance status for a specific date using the APP API.

        Args:
            date (str, optional): The date for which you want to retrieve attendance status. 
                If not provided, the current date is used. If the provided date is a Sunday, 
                the data for the previous day (Saturday) will be retrieved.

        Returns:
            str: A JSON string containing the attendance status.

        Raises:
            Exception: If there's an error decoding the JSON response.
        '''

        studentsysid = self.studentsysid

        if date is None:
            date = datetime.datetime.today().strftime('%d/%m/%Y')
        else:
            try:
                parsed_date = datetime.datetime.strptime(date, '%d/%m/%Y')
            except ValueError:
                raise ValueError(
                    "Invalid date format. Please use 'dd/mm/yyyy'.")

            # Check if the parsed date is a Sunday (weekday() returns 6 for Sunday)
            if parsed_date.weekday() == 6:
                # Adjust the date to the previous day (Saturday)
                parsed_date -= datetime.timedelta(days=1)
                date = parsed_date.strftime('%d/%m/%Y')

        payload = {
            "EPara1": self.E_PARA1,
            "EPara2": str(studentsysid),  # studentsysid
            "EPara3": date,  # date,
            "EPara4": str(self.password)
        }
        response = requests.post(
            f"{self.BASE_URL}/api/Water/eMethod347", data=json.dumps(payload))

        try:
            response = response.json()

            attendance_status_data = response['tblActualTimeTable']

            return attendance_status_data

        except:
            raise Exception(
                "Error Decoding JSON Response")
