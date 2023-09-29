![Logo](https://i.imgur.com/bcsXDdX.png)

<div style="text-align:center;">
  <a href="https://github.com/aditya76-git">aditya76-git</a> /
  <a href="https://github.com/aditya76-git/charusat-unofficial-api">charusat-unofficial-api</a>
</div>

<br />

<!-- <img src="https://i.imgur.com/y3L6XfN.png" align="right" /> -->

# CHARUSAT UnOfficial API

Unofficial scraper for accessing student information from Charusat University's website.

Provides methods to interact with the university's website, retrieve student details, attendance, timetable, fees, and more.

## 📋Details

- 👤 [Get User Details](#get-user-details)
- 📊 [Get Lecture Gross Attendance](#get-lecture-gross-attendance)
- 📋 [Get Attendance Status](#get-attendance-status)
- 💲 [Get Fees Details](#get-fees-details)

## ⚠️ Disclaimer

Please note that the `charusat_scraper` package is provided as-is and is not officially endorsed or supported by `CHARUSAT`. We have taken care to ensure that the package interacts with CHARUSAT Website in a secure and compliant manner

By using the `charusat_scraper` package, you acknowledge and agree that you are responsible for any actions taken with your CHARUSAT account, and you use the package at your own risk. We recommend using the package responsibly

We are not liable for any potential consequences that may arise from using the `charusat_scraper` package, including but not limited to `account suspension`, `data loss`, or any other `issues` related to your `CHARUSAT` account.

It's important to exercise `caution` and ensure that you keep your `username`, and `password` values `private` and `secure`.

The only way anyone can access your `CHARUSAT` account is by your Username and Password, so keep it safe with you. Refrain yourself from sharing with anyone else

## 📌 Note

Please note the following important information about the `charusat_scraper` package, which is a package for retrieving user data, including fees details, lecture gross attendance, attendance status, timetable, and other information:

This package empowers developers to harness its capabilities in creating insightful data representations, such as graphs and other visualizations, to gain deeper insights into attendance trends, fee structures, and other data.

1. **Security**: Your E-governance account can only be accessed using your username and password. Please refrain from sharing your login credentials with anyone, as it could compromise the security of your account. Avoid pasting anything into your browser's developer tools, as this action could potentially expose your cookies to unauthorized parties.

2. **Usage**: Ensure that you only use this package with the correct username and password. Repeatedly attempting to access your account with incorrect credentials may result in your account being temporarily blocked after five unsuccessful login attempts.

3. **Transparency**: This is a complete open-source project, and developers are encouraged to review the code to confirm that there are no external servers or intermediaries involved.We want you to have full confidence in the security and transparency of this package. If you have any doubts, we welcome you to explore the codebase for reassurance, and if you still have concerns, we recommend refraining from using this repository.

4. **Data Security** : This package interacts with the CHARUSAT E-Governance website in a manner similar to how a regular user would do using their mobile or PC. It performs actions programmatically and allows you to conveniently obtain useful parsed data, ensuring a safe and familiar browsing experience.

We encourage responsible and secure use of this package for accessing and managing your educational information.

## ⚙️Installation

Open your terminal or command prompt and enter the following command:

```bash
pip install git+https://github.com/aditya76-git/charusat-unofficial-api@main
```

> **Note:** To use this package you need to have a Active Charusat E-Governance Account

## 🚀Initialization

Initialize an instance of the `CharusatScraper` class by providing your Charusat E-Governance username and password as arguments. Replace `"YOUR_USERNAME"` and `"YOUR_PASSWORD"` with your actual Charusat login credentials.

```python3
from charusat_scraper import CharusatScraper
scraper = CharusatScraper("YOUR_USERNAME", "YOUR_PASSWORD")
```

## <a id="get-user-details"></a>➡️ Get User Details

Get User information and Previous Exam Details of the authenticated User

```python3
scraper.get_user_details()
```

Sample Result

```
{
    "user_info": {
        "id": "21CE00",
        "registrationDate": "24/09/2021",
        "admissionDate": "24/09/2021",
        "displayName": "DISPLAY NAME",
        "gender": "Male",
        "nationality": "INDIAN",
        "motherTongue": "HINDI",
        "birthDate": "00/00/0000",
        "birthplace": "PLACE",
        "address": "ADDRESS"
    },
    "previous_exam_details": [
        {
            "exam": "SSC",
            "seatNo.": "000000",
            "cgpa_percentageObtained": "85.4",
            "percentile": "0.00",
            "year": "2019",
            "month": "MAY",
            "board_University": "C.B.S.E",
            "group_Specialisation": "GENERAL"
        },
        {
            "exam": "HSC",
            "seatNo.": "000000",
            "cgpa_percentageObtained": "72.6",
            "percentile": "0.00",
            "year": "2021",
            "month": "MAY",
            "board_University": "C.B.S.E",
            "group_Specialisation": "SCIENCE (A GROUP)"
        }
    ]
}
```

## <a id="get-lecture-gross-attendance"></a>➡️ Get Lecture Gross Attendance

Get Gross Lecture Attendance information of the authenticated User

```python3
scraper.get_attendance()
```

Sample Result

```
[
    {
        "courseCode": "CE391 / PDA",
        "courseName": "PYTHON FOR DATA ANALYTICS",
        "classType": "LECT",
        "attendance": "12/15",
        "percentage": "80%"
    },
    {
        "courseCode": "CE391 / PDA",
        "courseName": "PYTHON FOR DATA ANALYTICS",
        "classType": "LAB",
        "attendance": "4/5",
        "percentage": "80%"
    },
    {
        "courseCode": "EE342 / SDCM",
        "courseName": "SYNCHRONOUS AND DC MACHINES",
        "classType": "LECT",
        "attendance": "20/26",
        "percentage": "76%"
    },
    {
        "courseCode": "EE342 / SDCM",
        "courseName": "SYNCHRONOUS AND DC MACHINES",
        "classType": "LAB",
        "attendance": "8/13",
        "percentage": "61%"
    },
    {
        "courseCode": "EE351 / EPTD",
        "courseName": "ELECTRICAL POWER TRANSMISSION AND DISTRIBUTION",
        "classType": "LECT",
        "attendance": "11/15",
        "percentage": "73%"
    },
    {
        "courseCode": "EE353 / PED-I",
        "courseName": "POWER ELECTRONICS AND DRIVES - I",
        "classType": "LECT",
        "attendance": "31/34",
        "percentage": "91%"
    },
    {
        "courseCode": "EE353 / PED-I",
        "courseName": "POWER ELECTRONICS AND DRIVES - I",
        "classType": "LAB",
        "attendance": "7/11",
        "percentage": "63%"
    },
    {
        "courseCode": "EE375 / ECAM",
        "courseName": "ENERGY CONSERVATION, AUDIT AND MANAGEMENT",
        "classType": "LECT",
        "attendance": "16/24",
        "percentage": "66%"
    },
    {
        "courseCode": "EE375 / ECAM",
        "courseName": "ENERGY CONSERVATION, AUDIT AND MANAGEMENT",
        "classType": "LAB",
        "attendance": "1/5",
        "percentage": "20%"
    },
    {
        "courseCode": "HS131.02 A / HS-5",
        "courseName": "COMMUNICATION AND SOFT SKILLS",
        "classType": "LAB",
        "attendance": "8/10",
        "percentage": "80%"
    }
]
```

## <a id="get-attendance-status"></a>➡️ Get Attendance Status

- Get Attendance Status of the authenticated User
- USES The APP API

```python3
scraper.get_attendance_status()
scraper.get_attendance_status(date = "22/09/2023")
```

Sample Result

```
[
    {
        "RowID": "4",
        "Message": "Success",
        "Status": 1,
        "TTDate": "21/09/2023",
        "TTTime": "09:10 - 10:09",
        "AttTaken": "P",
        "FacultyName": "FACULTY NAME",
        "Subjectdet": "0000 / PED-I",
        "StudentDetails": "BTECH(EE) / SEM 5 / DIV-I",
        "dayType": "T",
        "Daymsg": ""
    },
    {
        "RowID": "1",
        "Message": "Success",
        "Status": 1,
        "TTDate": "21/09/2023",
        "TTTime": "10:10 - 11:09",
        "AttTaken": "P",
        "FacultyName": "FACULTY NAME",
        "Subjectdet": "0000 / EPTD",
        "StudentDetails": "BTECH(EE) / SEM 5 / DIV-I",
        "dayType": "T",
        "Daymsg": ""
    },
    {
        "RowID": "2",
        "Message": "Success",
        "Status": 1,
        "TTDate": "21/09/2023",
        "TTTime": "12:10 - 14:09",
        "AttTaken": "P",
        "FacultyName": "FACULTY NAME",
        "Subjectdet": "0000 / SDCM",
        "StudentDetails": "BTECH(EE) / SEM 5 / DIV-I / A1",
        "dayType": "T",
        "Daymsg": ""
    },
    {
        "RowID": "3",
        "Message": "Success",
        "Status": 1,
        "TTDate": "21/09/2023",
        "TTTime": "14:20 - 16:20",
        "AttTaken": "P",
        "FacultyName": "FACULTY NAME",
        "Subjectdet": "0000 / ECAM",
        "StudentDetails": "BTECH(EE) / SEM 5 / DIV-I",
        "dayType": "T",
        "Daymsg": ""
    },
    {
        "RowID": "5",
        "Message": "Success",
        "Status": 1,
        "TTDate": "21/09/2023",
        "TTTime": "16:20 - 18:19",
        "AttTaken": "-",
        "FacultyName": "FACULTY NAME",
        "Subjectdet": "0000 / PDA",
        "StudentDetails": "BTECH(EE) / SEM 5 / DIV-I / A1",
        "dayType": "T",
        "Daymsg": ""
    }
]
```

## <a id="get-fees-details"></a>➡️ Get Fees Details

Get Fees Details of the authenticated User

```python3
scraper.get_fees_details()
```

Sample Result

```
[
    {
        "semester": "5",
        "totalFees": "00000.00",
        "recievedFees": "00000.00",
        "scholarshipAmount": "0.00",
        "pendingFees": "0.00"
    },
    {
        "semester": "4",
        "totalFees": "00000.00",
        "recievedFees": "00000.00",
        "scholarshipAmount": "0.00",
        "pendingFees": "0.00"
    },
    {
        "semester": "3",
        "totalFees": "00000.00",
        "recievedFees": "00000.00",
        "scholarshipAmount": "0.00",
        "pendingFees": "0.00"
    },
    {
        "semester": "2",
        "totalFees": "00000.00",
        "recievedFees": "00000.00",
        "scholarshipAmount": "0.00",
        "pendingFees": "0.00"
    },
    {
        "semester": "1",
        "totalFees": "00000.00",
        "recievedFees": "00000.00",
        "scholarshipAmount": "0.00",
        "pendingFees": "0.00"
    }
]
```

## <a id="get-result-data"></a>➡️ Get Result Details

<!-- **The inclusion of **VIEWSTATE, **VIEWSTATEGENERATOR, and \_\_EVENTVALIDATION in the payload is currently ineffective, rendering this method non-functional at the moment.** -->

- Get Result Details of the authenticated User
- USES The APP API

```python3
scraper.get_result_data()
scraper.get_result_data(sem = 4, month_year = "April 2023")
```

Sample Result

```
{
    "result": [
        {
            "courseName": "ENGINEERING MECHANICS",
            "courseCode": "CL143",
            "padagoggy": "THEORY",
            "credit": "3.00",
            "grade": "AA",
            "parentSubjectID": "7662"
        },
        {
            "courseName": "ENGINEERING MECHANICS",
            "courseCode": "CL143",
            "padagoggy": "PRACTICAL",
            "credit": "1.00",
            "grade": "AB",
            "parentSubjectID": "7662"
        },
        {
            "courseName": "ENVIRONMENTAL SCIENCES",
            "courseCode": "CL144.01 A",
            "padagoggy": "PRACTICAL",
            "credit": "2.00",
            "grade": "AB",
            "parentSubjectID": "7983"
        },
        {
            "courseName": "FOUNDATION COURSE ON MATHEMATICS AND PHYSICS",
            "courseCode": "FS101A",
            "padagoggy": "PRACTICAL",
            "credit": "2.00",
            "grade": "AA",
            "parentSubjectID": "8123"
        },
        {
            "courseName": "COMMUNICATIVE ENGLISH",
            "courseCode": "HS101.02 A",
            "padagoggy": "PRACTICAL",
            "credit": "2.00",
            "grade": "AB",
            "parentSubjectID": "7811"
        },
        {
            "courseName": "ENGINEERING MATHEMATICS-I",
            "courseCode": "MA143",
            "padagoggy": "THEORY",
            "credit": "4.00",
            "grade": "AA",
            "parentSubjectID": "7653"
        },
        {
            "courseName": "WORKSHOP PRACTICES",
            "courseCode": "ME142",
            "padagoggy": "PRACTICAL",
            "credit": "1.00",
            "grade": "AA",
            "parentSubjectID": "5774"
        },
        {
            "courseName": "ENGINEERING GRAPHICS",
            "courseCode": "ME146",
            "padagoggy": "THEORY",
            "credit": "2.00",
            "grade": "AB",
            "parentSubjectID": "7660"
        },
        {
            "courseName": "ENGINEERING GRAPHICS",
            "courseCode": "ME146",
            "padagoggy": "PRACTICAL",
            "credit": "1.00",
            "grade": "AA",
            "parentSubjectID": "7660"
        },
        {
            "courseName": "ENGINEERING PHYSICS-I",
            "courseCode": "PY142",
            "padagoggy": "PRACTICAL",
            "credit": "2.00",
            "grade": "BB",
            "parentSubjectID": "7961"
        }
    ],
    "summary": [
        {
            "studentName": "STUDENT NAME",
            "studentID": "STUDENT ID",
            "facultyName": "FACULTY OF TECHNOLOGY AND ENGINEERING",
            "date": "23/02/2022",
            "program": "B.TECH. (ELECTRICAL)",
            "examMonthYear": "February 2022",
            "studentType": "FRESHER",
            "totalCredits": "20.00",
            "creditEarned": "20.00",
            "sgpa": "9.45",
            "cgpa": "9.45",
            "noofbacklog": "0.00",
            "studentLastSem": "8"
        }
    ]
}
```

## 🌟 Show Your Support

- If you find this project useful or interesting, please consider giving it a star on GitHub. It's a simple way to show your support and help others discover the project.

![Github Stars](https://img.shields.io/github/stars/aditya76-git/charusat-unofficial-api?style=social "Github Stars")

## 👨‍💻Developement

Thank you for your interest in contributing to this project! There are several ways you can get involved:

- **Opening Issues**: If you encounter a bug, have a feature request, or want to suggest an improvement, please open an issue. We appreciate your feedback!
- **Cloning the Project**: To work on the project locally, you can clone the repository by running:

```bash
git clone https://github.com/aditya76-git/charusat-unofficial-api.git
```

- **Sending Pull Requests**: If you'd like to contribute directly to the codebase, you can fork the repository, make your changes, and then send a pull request. We welcome your contributions!

## Contributors

A Big **Thanks** to those who helped make our project better.

**Gautam Mehta**

- GitHub: [@coderGtm](https://github.com/coderGtm)

## 💻Authors

- Copyright © 2023 - [aditya76-git](https://github.com/aditya76-git) / [charusat-unofficial-api](https://github.com/aditya76-git/charusat-unofficial-api)
