import requests

base_url = 'http://127.0.0.1:8000/api/'

username='Murphy'
password='test123'

# Retrieve all courses
result = requests.get(f'{base_url}courses/')
courses = result.json()

available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses: {available_courses}')

#Enroll users onto all availables courses
for course in courses:
    course_id = course['id']
    course_title = course['title']
    response = requests.post(f'{base_url}courses/{course_id}/enroll/', auth=(username, password))
    if response.status_code == 200:
        # successful request
        print(f'Successfully enrolled in {course_title}')