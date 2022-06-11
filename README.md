# Elearning-app
E-learning application that allows instructors to create and manage courses for students with RestfulAPI integration powered by Python, Django, and Django Rest Framework

<h2>Sections</h2>
<p>
  <ul>
    <li><a href="#desc">Project Description</a></li>
    <li><a href="#feat">Features</a></li>
    <li><a href="#tech">Technology</a></li>
    <li><a href="#setup">Setup</a></li>
    <li><a href="#status">Project Status</a></li>
    <li><a href="#contribute">Contributing</a></li>
    <li><a href="#contact">Author</a></li>
    <li><a href="#licence">Licence</a></li>
   </ul>
</p>

<h2 id="desc">Project Description</h2>
<p> This Django project is an Elearning platform where students can signup and enroll on a course. Course Instructors can also signup and and request Instructors status to create
and manage course contents for students. 
</p>

<h2 id="feat">Features</h2>
<ul>
  <li>Student/Instructor Registration and Authentication</li>
  <li>Content Management System(CMS)</li>
  <li>Course Forum</>
  <li>Caching</li>
</ul>

<h2 id="tech">Technology</h2>
<ul>
  <li>Python</li>
  <li>Django</li>
  <li>Django Rest Framework(DRF)</li>
  <li>Django Channels</i>
  <li>Postgresql</li>
  <li>HTML5</li>
  <li>CSS3</li>
  <li>Redis</li>
</ul>

<h2 href=#setup>Setup</h2>
To run the application, please follow guidlines below
<p>
1. Requirements
 <ul>
  <li>You need a PC or Macbook</li>
  <li>You have Git installed</li>
  <li>A Text Editor or IDE(eg.Vscode, Sublime, Pycharm)</li>
</ul></p>
<p>2. Install python3 and Pipenv</p>

<p>3. Now you setup as indicated below:</p>


 ```
  # Clone this repository into the directory of your choice
  $ git clone https://github.com/KwabenaYeboah/Elearning-app.git
  
  # Move into project folder
  $ cd blog-application
  
  # Install from Pipfile
  $ pipenv install
  
  # Migrate database models
  (Elearning-app-xxx) $ python manage.py migrate
  
  # Create superuser account
  (Elearning-app-XXXX) $ python manage.py createsuperuser
  
  # start server
  (Elearning-app-XXXX) $  python manage.py runserver
  
  # Copy the IP address provided once your server is up and running. (you will see something like >> Serving at 127.0.0.1....)
  
  # Open the address in the browser
  >>> http://127.0.0.1:8000/
  
  # Django Admin
  >>> http://127.0.0.1:8000/admin/
  ```

<h2 id="status">Project Status</h2>
Project is: Done

<h2 id="contribute">Contributing</h2>
Pull requests and stars are always welcome

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

<h2 id="contact">Author</h2>

[KwabenaYeboah](https://github.com/KwabenaYeboah/)

<h2 id="licence">Licence</h2>

  **MIT** Licence
