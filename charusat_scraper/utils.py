import re
from bs4 import BeautifulSoup
import json


def parse_user_info(html):
    '''
    Parse user information from HTML and return it as a dictionary.

    Args:
        html (str): The HTML content containing user information.

    Returns:
        dict: A dictionary containing parsed user information with the following keys:
            - 'id': User ID
            - 'registrationDate': Registration date
            - 'admissionDate': Date of admission
            - 'displayName': Display name
            - 'gender': Gender
            - 'nationality': Nationality
            - 'motherTongue': Mother tongue
            - 'birthDate': Birth date
            - 'birthplace': Birthplace
            - 'personalEmail': Personal email
            - 'address': Complete address including pincode

    Note:
        If any of the fields are not found in the HTML, they won't be included in the
        returned dictionary.
    '''
    soup = BeautifulSoup(html, 'html.parser')

    data = {}

    # Define a dictionary of field names and corresponding keys
    fields = {
        'ctl00$ContentPlaceHolder1$txtIDNo': 'id',
        'ctl00$ContentPlaceHolder1$txtRegDate': 'registrationDate',
        'ctl00$ContentPlaceHolder1$txtDateOfAdmission': 'admissionDate',
        'ctl00$ContentPlaceHolder1$txtDisplayName': 'displayName',
        'ctl00$ContentPlaceHolder1$rbtGender': 'gender',
        'ctl00$ContentPlaceHolder1$txtNationality': 'nationality',
        'ctl00$ContentPlaceHolder1$txtMotherTongue': 'motherTongue',
        'ctl00$ContentPlaceHolder1$txtBirthDate': 'birthDate',
        'ctl00$ContentPlaceHolder1$txtBirthPlace': 'birthplace',
        'ctl00_ContentPlaceHolder1_reference1_Address1_lblEmailPersonal': 'personalEmail',
    }

    # Extract values for the defined fields
    for field_name, key in fields.items():
        input_field = soup.find('input', {'name': field_name})
        if input_field:
            data[key] = input_field.get('value')

    # Extract and combine address parts
    address_parts = []
    for field_name in [
        'ctl00$ContentPlaceHolder1$reference1$Address1$txtAddress1',
        'ctl00$ContentPlaceHolder1$reference1$Address1$txtAddress2',
        'ctl00$ContentPlaceHolder1$reference1$Address1$txtAddress3',
        'ctl00$ContentPlaceHolder1$reference1$Address1$txtCity',
        'ctl00$ContentPlaceHolder1$reference1$Address1$txtState',
    ]:
        input_field = soup.find('input', {'name': field_name})
        if input_field:
            address_parts.append(input_field.get('value'))

    # Combine the address parts and add the pincode
    address = ' '.join(address_parts)
    pincode = soup.find('input', {'name': 'ctl00$ContentPlaceHolder1$AD2$txtPincode'})
    if pincode:
        address += " - " + pincode.get('value')

    data['address'] = address

    return data


def to_camel_case(text):
    '''
    Convert a given text into camel case.

    This function takes a string as input and converts it into camel case,
    where words are joined without spaces, and each word except the first
    is capitalized. Special characters like '%' and '/' are replaced with
    underscores.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The camel-cased version of the input text.
    '''
    text = text.replace("%", "Percentage").replace("/", "_")
    words = text.split()
    if len(words) > 1:
        return words[0].lower() + ''.join(x.capitalize() or '_' for x in words[1:]).replace("/", "_")
    else:
        return text.lower()


def parse_previous_exam_details(html):
    '''
    Parse HTML containing previous exam details and convert it into a list of dictionaries.

    Args:
        html (str): The HTML content to be parsed.

    Returns:
        A JSON-formatted string representing the Previous Exam details.
    '''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(
        'table', {'id': 'ctl00_ContentPlaceHolder1_gv_tblEducation'})

    headers = [to_camel_case(th.text.strip()) for th in table.find_all('th')]
    data = []

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        item = {}

        for i, col in enumerate(columns):
            key = headers[i]
            value = col.text.strip()

            if not "Select..." in value and key and value:
                item[key] = value

        if item:  # Exclude rows with no data
            data.append(item)

    return data


def parse_fees_data(html_data):
    '''
    Parse HTML containing fees details and convert it into a JSON string.

    Args:
        html_data (str): The HTML content to be parsed.

    Returns:
        A JSON-formatted string representing the fees details.
    '''
    soup = BeautifulSoup(html_data, 'html.parser')

    fees_table = soup.find('table', {'id': 'gvfees_details'})

    fees_data = []

    rows = fees_table.find_all('tr')[1:]

    for row in rows:
        # Extract data from each row
        columns = row.find_all('td')
        semester = columns[0].text.strip()
        total_fees = columns[1].text.strip()
        received_fees = columns[2].text.strip()
        scholarship_amt = columns[3].text.strip()
        pending_fees = columns[4].text.strip()

        entry = {
            'semester': semester,
            'totalFees': total_fees,
            'recievedFees': received_fees,
            'scholarshipAmount': scholarship_amt,
            'pendingFees': pending_fees
        }

        # Create a dictionary for each row and append it to the list
        fees_data.append(entry)

    return json.dumps(fees_data, indent=4)


def parse_result_data(html):
    '''
    Parse HTML containing student result data and convert it into a JSON string.

    Args:
        html (str): The HTML content to be parsed.

    Returns:
        A JSON-formatted string representing the student's result data.

    '''
    soup = BeautifulSoup(html, 'html.parser')
    result_data = {}

    # Find the table with result data (id='gvresult')
    result_table = soup.find('table', {'id': 'gvresult'})
    if result_table:
        result_data['result'] = []
        rows = result_table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 4:
                course_data = {
                    'courseName': columns[0].text.strip(),
                    'courseType': columns[1].text.strip(),
                    'credit': columns[2].text.strip(),
                    'grade': columns[3].text.strip(),
                }
                result_data['result'].append(course_data)

    # Find the table with Month/Year, Total Credit, Credits Earned (id='gvresult1')
    result_table1 = soup.find('table', {'id': 'gvresult1'})
    if result_table1:
        result_data['summary'] = []
        rows = result_table1.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 4:
                summary_data = {
                    'semester': soup.find('span', {'id': 'lblSem'}).text,
                    'month_year': columns[0].text.strip(),
                    'totalCredits': columns[1].text.strip(),
                    'creditsEarned': columns[2].text.strip(),
                    'sgpa': columns[3].text.strip()
                }
                result_data['summary'].append(summary_data)

    student_data = {}  # Initialize an empty dictionary for student data

    student_data['name'] = soup.find('span', {'id': 'lblStudentName'}).text
    student_data['id'] = soup.find('span', {'id': 'lblStudentID'}).text

    result_data['student_info'] = student_data

    return json.dumps(result_data, indent=4)


def extract_payload_values_for_results(html):
    pattern = r'__(?P<name>VIEWSTATE|VIEWSTATEGENERATOR|EVENTVALIDATION)\|(?P<value>[^|]+)'
    matches = re.finditer(pattern, html)

    result = {match.group('name'): match.group('value') for match in matches}

    return result


def extract_payload_values(text):
    pattern = r'<input[^>]*name=("__VIEWSTATEGENERATOR"|"__EVENTVALIDATION"|"__VIEWSTATE")[^>]*value="([^"]*)"'

    matches = re.findall(pattern, text)

    values = {key.strip('"'): value for key, value in matches}

    return values


def parse_attendance_status_html(html):
    '''
    Parse HTML containing Attendance Status details and convert it into a JSON string.

    Args:
        html_data (str): The HTML content to be parsed.

    Returns:
        A JSON-formatted string representing the Time Table details.
    '''
    soup = BeautifulSoup(html, 'html.parser')

    timetable_table = soup.find('table', {'id': 'gvtimetableDetails'})

    fullform_table = soup.find('table', {'id': 'gvfullform'})

    json_data = []

    for row in timetable_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        time = columns[0].text.strip()
        faculty = columns[1].text.strip()
        course_code = columns[2].text.strip()
        attendance_status = columns[3].text.strip()

        course_name_row = fullform_table.find('td', string=course_code)
        if course_name_row:
            course_name = course_name_row.find_next('td').text.strip()
        else:
            course_name = ''

        entry = {
            'time': time,
            'faculty': faculty,
            'courseCode': course_code,
            'courseName': course_name,
            'attendanceStatus': attendance_status
        }

        # Create a dictionary for each row and append it to the list
        json_data.append(entry)

    return json.dumps(json_data, indent=4)


def parse_attendance_html(html):
    '''
    Parse HTML containing Overall Gross Lecture Attendance details and convert it into a JSON string.

    Args:
        html_data (str): The HTML content to be parsed.

    Returns:
        A JSON-formatted string representing the Overall Gross Lecture Attendancedetails.
    '''
    soup = BeautifulSoup(html, 'html.parser')

    # Find the first table with id "gvGrossAttPop"
    gross_attendance_table = soup.find('table', {'id': 'gvGrossAttPop'})

    # Find the second table with id "gvGAttSubjectsPop"
    course_name_table = soup.find('table', {'id': 'gvGAttSubjectsPop'})

    json_data = []
    lecture_gross_text = soup.find("span", {"id" : "lblHeadAnnouncement"}).text
    semester = lecture_gross_text[lecture_gross_text.find("Semester ")+len("Semester ") : lecture_gross_text.find("Semester ")+len("Semester ")+2]
    lecture_gross_attendance = lecture_gross_text[lecture_gross_text.find("- ")+len("- "):lecture_gross_text.find("%")-1]

    # Skip the header row
    for row in gross_attendance_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        course_code = columns[0].find('span').text.strip()
        class_type = columns[1].find('span').text.strip()
        present_total = columns[2].text.replace(
            '\n', '').replace('\r', '').replace(' ', '').strip()
        percentage = columns[3].text.strip()

        course_name_row = course_name_table.find('td', string=course_code)
        if course_name_row:
            course_name = course_name_row.find_next('td').text.strip()
        else:
            course_name = ''

        entry = {
            'courseCode': course_code,
            'courseName': course_name,
            'classType': class_type,
            'attendance': present_total,
            'percentage': percentage
        }
        json_data.append(entry)
    
    json_data.append({"Lecture Gross":lecture_gross_attendance+"%", "Semester":semester})

    return json.dumps(json_data, indent=4)
