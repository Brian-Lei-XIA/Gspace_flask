import datetime
import os
import pymysql
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user,current_user
from flask import Flask, render_template, request, redirect, abort, session, flash, url_for, send_from_directory
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, SubmitField, IntegerField
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, email_validator, NumberRange
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import *


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

bootstrap = Bootstrap(app)
app.secret_key = os.urandom(16)
app.config["SECRET_KEY"] = 'A-VERY-LONG-SECRET-KEY'
app.config['UPLOAD_FOLDER'] = '%s/static/upload' % os.getcwd()
#app.config["RECAPTCHA_PUBLIC_KEY"] = 'A-VERY-LONG-SECRET-KEY'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])    



def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
            return decorated_function
    return decorator


#this class provide a from for register
class Registerform(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=6, max=20)])
    age = IntegerField('age', validators=[DataRequired(), NumberRange(min=7, max=18)])
    gender = SelectField('gender',
        choices = [('F', 'Female'), ('M', 'Male')],
        default = 'Female'
    )
    phoneNum = StringField('phoneNum', validators=[DataRequired(), Length(min=7, max=13)])
    email = StringField('email', validators=[DataRequired(), Email()])
    avatar = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('register')


#this class provide a form for teacher to grading assignment
class Grade(FlaskForm):
    grade = StringField('grade')


#this class provide a from for edit user information
class editForm(Form):
    name = StringField('name')
    age = StringField('age')
    gender = SelectField('gender',
        choices = [('F', 'Female'), ('M', 'Male')],
        default = 'Female'
    )
    phoneNum = StringField('phoneNum')
    email = StringField('email')
    avatar = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


#this class provide a from for user login
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired()])
    
#this class provide a from for user add form    
class addForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(min=10, max=10)])


#USERMIXIN      
#this class used to record user's role    
class User(UserMixin):    
    def __init__(self, id):
        database = DatabaseOperations()
        self.id = id
        self.name = id
        self.password = database.get_password(id)
        database.__del__
        if self.name[0] == 'S':
            self.role ='Student'
        if self.name[0] == 'A':
            self.role = 'Administrator'
        if self.name[0] == 'T':
            self.role = 'Teacher'
        self.id = database.get_id(self.name,self.name)


#we designd some database operations:
#check_user_name/#getInfomation/#get_password/#get_id/#update/#getBySql/#insert/#insert3
class DatabaseOperations():
    # Fill in the information of your database server.
    __db_url = 'localhost'
    __db_username = 'root'
    __db_password = ''
    __db_name = 'gspace2'
    __db = ''

    def __init__(self):
        """Connect to database when the object is created."""
        self.__db = self.db_connect()

    def __del__(self):
        """Disconnect from database when the object is destroyed."""
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username, self.__db_password, self.__db_name)
        return self.__db
    
    #check the userName in the database, if userName found return it
    def check_user_name(self, username):
        sql = """
        select username
        from account
        where username  = '%s'
        """ % (username)
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result[0][0]
        except:
            print("Can not access database")

    #get the information by the role
    def getInfomation(self, id):
        sql = '''
            select *
            from %s
            where userName = '%s'
        '''%(session.get('role'),id)
        try:
            self.db_connect()
            cursor = self.__db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            infor = []
            for i in range(1, 9):
                infor.append(result[0][i])
            self.__del__
            return infor
        except:
            print("Can not access database")

    #get password
    def get_password(self, username):
        sql = """
            select password
            from account
            where username  = '%s'
        """ % (username)
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result[0][0]
        except:
            print("Can not access database")

    #get id
    def get_id(self, username, role):
        sql = """
            select id
            from %s
            where userName  = '%s'
        """ % (role, username)
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result[0][0]
        except:
            print("Can not access database")

    #input sql and update database
    def update(self, sql):
        self.db_connect
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            self.__db.commit()
            print("Update Success!")
        except:
            self.__db.rollback()
            print("Update Fail!")
        self.__db.close()
    
    #input sql and out put result 
    def getBySql(self, sql):
        self.db_connect
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except:
            self.__db.rollback()
  
    #insert sql and out put result 
    def insert(self, sql):
        self.db_connect
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            self.__db.commit()
            print("Insert Success!")
        except:
            self.__db.rollback()
            print("Insert Fail!")
        self.__db.close()
        
    #conduct three sql function
    def insert3(self, sql1, sql2, sql3):
        self.db_connect
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            self.__db.commit()
            print("insert success")
        except:
            self.__db.rollback()
            print("insert fail")  


#------------------------------------------------------------------------------------------------------------------------------------------
#LOGIN
#this route is for user login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #connect with database
        database = DatabaseOperations()
        database.db_connect()

        #get input username and input password
        form = LoginForm(request.form)
        inputUsername = form.username.data
        inputPassword = form.password.data

        #search the username in the database
        checkusername = database.check_user_name(inputUsername)

        #if no username march
        if not checkusername:
            message = "Please check your username"
            return render_template('login.html', message=message)
        user = User(inputUsername)
        #check if the password matches
        if inputPassword == user.password:
            login_user(user)
            session['role'] = user.role
            session['userName'] = user.name
            session['id'] = database.get_id(user.name,user.role)
            # Exit this function by redirect to the next page.
            page = ('./%s_Homepage')%user.role
            return redirect(page)
        else:
            message = "Please check your username and password"
            return render_template('login.html', message=message)
    return render_template('login.html')


#return 404 if the object is unfind
@app.route('/404')
def error():
    return render_template('404.html')


#this route can return the address of the file we saved
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#this route is for student to registe
@app.route('/stu_Register', methods=['GET', 'POST'])
def stu_Register():
    form = Registerform(CombinedMultiDict([request.form, request.files]))
    if form.validate_on_submit() and request.method == 'POST':
        #get user input
        #(for image/file: read and save it firstly ,then get address and save it in the database)
        name = form.name.data
        age = form.age.data
        gender = form.gender.data
        email = form.email.data
        phone = form.phoneNum.data
        avatarfile = form.avatar.data
        print(avatarfile)
        filename = secure_filename(avatarfile.filename)
        print(filename)
        avatarfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image =  url_for('uploaded_file', filename=filename)
        print(image)
        
        database = DatabaseOperations()
        
        #create new account and password
        maxid = database.getBySql("""select max(id) from student""")
        nextID = maxid[0][0] + 1
        print(nextID)
        if len(str(nextID)) == 5:
            userName = 'S8300' + str(nextID)
            print(userName)
        elif len(str(nextID)) == 6:
            userName = 'S8300' + str(nextID)
            print(userName)
        elif len(str(nextID)) == 7:
            userName = 'S83' + str(nextID)
            print(userName)
        elif len(str(nextID)) > 7:
            flash('The maximum number of people has been reached!')
            return redirect(url_for('login'))
        
        #insert new students
        insertStu = """
        insert into student (name, gender, age, email, phone, avatar, username, slevel)
        values ('%s', '%s', %d, '%s', '%s','%s','%s', 1)
        """ % (name, gender, age, email, phone, image, userName)
        database.insert(insertStu)
        
        #return account and password create by system to user
        flash('Registered successfully!')
        flash("Account:%s" % userName)
        flash("Password:%s" % userName)
        return redirect(url_for('login'))
    return render_template('stu_Register.html', form = form)



#------------------------------------------------------------------------------------------------------------------------------------------
#STUDENT
#Student Home Page
#Function:
'''
1. The brief infor of the class
2. The coming classes
3. The link to each class
'''
@app.route('/Student_Homepage')
@login_required
def student_homepage():
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    #SQL
    #coming Class
    comingClassSql = '''
    select courseName, lectureDate,lectureStartTime,lectureEndTime
    from havecourse, havelecture, lecture, course
    where havecourse.classID = havelecture.classID AND havelecture.lectureId = lecture.lectureID AND course.courseID = havelecture.courseID AND sid = %d
    order by lectureDate, lectureStartTime
    limit 5
    ''' % session.get('id')
    #Course
    courseSql = '''
        select courseName, classID
        from havecourse as HC, course as CO
        where HC.courseId = CO.courseId AND sid =  %d
    ''' % session.get('id')
    #Total Class NUM
    totalClassSQL = '''
        select count(classid)
        from havecourse
        where sid = %s
    ''' % session.get('id')
    #Reminding homework Num
    reHomeworkSQL = '''
        select count(lectureid)
        from assignment
        where sid = %s AND status = '0'
    ''' % session.get('id')

    #Database Operations
    database = DatabaseOperations()
    classSchedule = database.getBySql(comingClassSql)
    course = database.getBySql(courseSql)
    totalClass = database.getBySql(totalClassSQL)
    reHomework = database.getBySql(reHomeworkSQL)
    lists=[]
    for i in range(len(classSchedule)):
        lists.append([])
    for i in range(len(classSchedule)):
        lists[i].append(classSchedule[i][0])
        lists[i].append(classSchedule[i][1])       
        lists[i].append(classSchedule[i][2])
        lists[i].append(classSchedule[i][3])
    return render_template('Student_Homepage.html',message = lists, course=course, totalClass = totalClass[0][0], reHomework = reHomework[0][0])


#Student Userpage
'''
Function:
1. Show the personal infor
2. Give the Edit Button to go to the Edit page
'''
@app.route('/Student_Userpage')
@login_required
def student_userpage():
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    #connect wiht database
    database = DatabaseOperations()
    #get information
    infor = database.getInfomation(session.get('userName'))
    print(session.get('userName'))
    database.db_connect()
    name = infor[0]
    gender = infor[1]
    age = infor[2]
    email = infor[3]
    phoneNum = infor[4]
    level = infor[7]
    photo = str(infor[5], encoding ='utf-8')
    form = editForm(request.form)
    return render_template('Student_Userpage.html', name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, photo = photo)


#Student User Infor Edit
'''
1. Edit the personal infor
2. Save to confire the change
3. Cancel to go bace
'''
@app.route('/Student_UserEditpage', methods=['GET', 'POST'])
@login_required
def student_usereditpage():
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    database = DatabaseOperations()
    infor = database.getInfomation(session.get('userName'))
    print(session.get('userName'))
    database.db_connect()
    name = infor[0]
    gender = infor[1]
    age = infor[2]
    email = infor[3]
    phoneNum = infor[4]
    preavatar = str(infor[5], encoding='utf-8')
    level = infor[7]

    form = editForm(CombinedMultiDict([request.form, request.files]))
    if request.method == 'POST' and form.validate():
        avatarfile = request.files["image"]
        print(avatarfile)
        filename = secure_filename(avatarfile.filename)
        print(filename)
        if filename == '':
            image = preavatar
        else:
            avatarfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = url_for('uploaded_file', filename=filename)
            print(image)

        sql = '''
        update student
        set name = '%s', age = %d, email = '%s', phone = '%s', gender = '%s', avatar = '%s'
        where userName = '%s'
        ''' %(form.name.data, int(form.age.data), form.email.data, form.phoneNum.data, form.gender.data, image, session.get('userName'))
        database = DatabaseOperations()
        database.update(sql)
        return redirect('Student_Userpage')
    return render_template('Student_UserEditpage.html',name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, preavatar=preavatar)


#Student Total Coursepage
'''
1. Show all the course a student have
2. Give the link for student to go to the class detail page
'''
@app.route('/Student_Coursepage')
@login_required
def student_coursepage():
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    #SQL
    #get the courses
    courseSql = '''
        select courseName, classID
        from havecourse as HC, course as CO
        where HC.courseId = CO.courseId AND sid =  %d
    ''' % session.get('id')
    #Database Operations
    database = DatabaseOperations()
    course = database.getBySql(courseSql)
    return render_template('Student_Coursepage.html',course = course)

#Class page
'''
Give the basic infor about a class include:
    * Coming classes time
    * Lecture brief
    * Assignment infor
    * Attendance infor
Func:
1. student can take attendacne
2. student can submit assignment
'''
@app.route('/Student_Classpage/<classId>')
@login_required
def Student_Classpage(classId):
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    #SQL
    #get the class Name
    classNameSQL = '''
    select className from class where classid = %s
    ''' % classId
    #因为coming Lecture返回的item会受时间影响，是时间晚于当前时间的
    #所以跟lecture不一样
    #但是因为这里数据库没有晚于当下时间的数据，所以暂时两个sql相同
    #get the coming classes
    comingLecSql = '''
    select lectureDate, lectureStartTime, lectureEndTime, lecturename
    from lecture
    where classID = %s
    order by lectureName
    limit 5
    ''' % classId

    #Get each lecture brief
    lectureDetailSQL = '''
    select lectureName, description
    from lecture
    where classid = %s
    '''  % classId

    #Get the attendace
    attendanceSQL = '''
    with temp as (
        select HL.lectureID, lectureDate, lectureStartTime,lectureEndTime
        from havelecture as HL, lecture as L
        where HL.classID = %s AND HL.classID = L.classID AND HL.lectureID = L.lectureID
    )
    select lectureDate, lectureStartTime, lectureEndTime,status,submitTime, T.lectureID
    from temp as T, attendance as A
    where T.lectureId = A.lectureId AND sid = %s
    ''' % (classId, session.get('id'))

    #Get the assignmet
    assignmentSQL = '''
    with temp as(
        select lectureId
        from havelecture
        where courseId = %s
    )
    select L.lectureName, assignmentDate, assignmnetStartTime, assignmentEndTime, assignmentGrade, status, submitTime, sID, temp.lectureId
    from lecture as L, assignment as A, temp
    where L.lectureId = A.lectureId AND L.lectureId = temp.lectureId AND sID = %s
    ''' % (classId,session.get('id'))

    #Database Operations
    database = DatabaseOperations()
    comingclasses = database.getBySql(comingLecSql)
    className = database.getBySql(classNameSQL)
    lectureDetail = database.getBySql(lectureDetailSQL)
    attendance = database.getBySql(attendanceSQL)
    assignment = database.getBySql(assignmentSQL)
    return render_template('Student_Classpage.html',coming = comingclasses, className = className, lectureDetail = lectureDetail, attendance = attendance, assignment = assignment, classID = classId)

#Student Submit Assignment
'''
Func:
1. Submit a assignment, upload the status and the submit time
'''
@app.route('/Student_Classpage/<classId>/subAs/<lectureId>')
@login_required
def SubmitAssignment(classId,lectureId):
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    #get the current time
    Time = datetime.now()
    #SQL
    #submit the assignment, it will update the status and the submitTime
    assignmentUpdate = '''
    update assignment
    set status = '1', submitTime = '%s'
    where sid = %s AND lectureId = %s
    ''' % (Time.strftime('%Y-%m-%d %H:%M:%S'), classId, lectureId)
    
    #Database Operations
    database = DatabaseOperations()
    database.update(assignmentUpdate)
    url = '/Student_Classpage/%s' % classId
    return redirect(url)

#Student Take Attendance
'''
Func:
1. Take Attendacne
'''
@app.route('/Student_Classpage/<classId>/takeAttendance/<lectureId>')
@login_required
def TakeAttendance(classId,lectureId):
    #check if the role is correct
    if session.get('role') != 'Student':
        return render_template('404.html')
    database = DatabaseOperations()
    Time = datetime.now()
    assignmentUpdate = '''
    update attendance
    set status = '1', submitTime = '%s'
    where sid = %s AND lectureId = '%s'
    ''' % (Time.strftime('%Y-%m-%d %H:%M:%S'), session.get('id'), lectureId)
    database.update(assignmentUpdate)
    url = '/Student_Classpage/%s' % classId
    return redirect(url)


#------------------------------------------------------------------------------------------------------------------------------------------
#ADMINISTRATOR
#this route is to return a review information to user
@app.route('/Administrator_Homepage')
@login_required
def admin_homepage():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allcourses = """ 
    select courseName, courseStartTime, courseEndTime, count(distinct tId), count(distinct sId), count(distinct classID)
    from course natural join havecourse natural join teachcourse
    group by courseName
    limit 10
    """
    allclasses = """
    select className, capacity, count(distinct tId), count(distinct sID)
    from class natural join havecourse natural join teachcourse
    group by classID
    limit 10
    """
    allteachers = """
    select name, gender, age, tlevel, phone, email
    from teacher
    limit 10    
    """
    allstudents = """
    select name, gender, age, slevel, phone, email
    from student
    limit 10
    """ 
    totalco = """
    select count(courseID)
    from course
    """
    totalcl = """
    select count(classID)
    from class
    """
    totaltea = """
    select count(id)
    from teacher
    """
    totalstu = """
    select count(id)
    from student
    """
    
    database = DatabaseOperations()
    allcoursesInfo = database.getBySql(allcourses)
    allclassesInfo = database.getBySql(allclasses)
    allteachersInfo = database.getBySql(allteachers)
    allstudentsInfo = database.getBySql(allstudents)
    totalcourse = database.getBySql(totalco)
    totalclass = database.getBySql(totalcl)
    totalteacher = database.getBySql(totaltea)
    totalstudent = database.getBySql(totalstu)

    #record all courses information
    list1=[]
    for i in range(len(allcoursesInfo)):
        list1.append([])
    for i in range(len(allcoursesInfo)):
        list1[i].append(allcoursesInfo[i][0])
        list1[i].append(allcoursesInfo[i][1])
        list1[i].append(allcoursesInfo[i][2])
        list1[i].append(allcoursesInfo[i][3])
        list1[i].append(allcoursesInfo[i][4])
        list1[i].append(allcoursesInfo[i][5])
    
    #record all classes information
    list2=[]
    for i in range(len(allclassesInfo)):
        list2.append([])
    for i in range(len(allclassesInfo)):
        list2[i].append(allclassesInfo[i][0])
        list2[i].append(allclassesInfo[i][1])
        list2[i].append(allclassesInfo[i][2])
        list2[i].append(allclassesInfo[i][3])
    
    #record all teachers information
    list3=[]
    for i in range(len(allteachersInfo)):
        list3.append([])
    for i in range(len(allteachersInfo)):
        list3[i].append(allteachersInfo[i][0])
        list3[i].append(allteachersInfo[i][1])
        list3[i].append(allteachersInfo[i][2])
        list3[i].append(allteachersInfo[i][3])
        list3[i].append(allteachersInfo[i][4])
        list3[i].append(allteachersInfo[i][5])
    
    #record all students information
    list4=[]
    for i in range(len(allstudentsInfo)):
        list4.append([])
    for i in range(len(allstudentsInfo)):
        list4[i].append(allstudentsInfo[i][0])
        list4[i].append(allstudentsInfo[i][1])
        list4[i].append(allstudentsInfo[i][2])
        list4[i].append(allstudentsInfo[i][3])
        list4[i].append(allstudentsInfo[i][4])
        list4[i].append(allstudentsInfo[i][5])
           
    return render_template('Administrator_Homepage.html', message1 = list1, message2 = list2, message3 = list3, message4 = list4, courNum = totalcourse, classNum = totalclass, studNum = totalstudent, teachNum = totalteacher)

#this route shows course information
@app.route('/Administrator_Coursespage')
@login_required
def admin_coursespage():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allcourses = """ 
    select courseID, courseName, courseStartTime, courseEndTime, count(distinct tId), count(distinct sId), count(distinct classID)
    from course natural join havecourse natural join teachcourse
    group by courseName
    """
    database = DatabaseOperations()
    allcoursesInfo = database.getBySql(allcourses)
    
    list1=[]
    for i in range(len(allcoursesInfo)):
        list1.append([])
    for i in range(len(allcoursesInfo)):
        list1[i].append(allcoursesInfo[i][0])
        list1[i].append(allcoursesInfo[i][1])
        list1[i].append(allcoursesInfo[i][2])
        list1[i].append(allcoursesInfo[i][3])
        list1[i].append(allcoursesInfo[i][4])
        list1[i].append(allcoursesInfo[i][5])
        list1[i].append(allcoursesInfo[i][6])
    return render_template('Administrator_Coursespage.html',  message1 = list1)

#this route is to show course information in course edit page 
@app.route('/Administrator_CoursespageEdit/<courseName>')
@login_required
def admin_coursespageEdit(courseName):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allcourses = """ 
    select courseName, courseStartTime, courseEndTime, count(distinct tId), count(distinct sId), count(distinct classID)
    from course natural join havecourse natural join teachcourse
    where courseName = '%s'
    group by courseName
    """ % (courseName)
    database = DatabaseOperations()
    allcoursesInfo = database.getBySql(allcourses)
    
    list1=[]
    for i in range(len(allcoursesInfo)):
        list1.append([])
    for i in range(len(allcoursesInfo)):
        list1[i].append(allcoursesInfo[i][0])
        list1[i].append(allcoursesInfo[i][1])
        list1[i].append(allcoursesInfo[i][2])
        list1[i].append(allcoursesInfo[i][3])
        list1[i].append(allcoursesInfo[i][4])
        list1[i].append(allcoursesInfo[i][5])
    return render_template('Administrator_CoursespageEdit.html', courseName=courseName, message1 = list1)


#this route is to delete course in course edit page
@app.route('/Administrator_CourseEdit/<id>/')
@login_required
def admin_delete_course(id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    delete = """
        delete from course where courseID = %d
    """ % (int(id))
    database = DatabaseOperations()
    database.update(delete)
    return redirect(url_for('admin_coursespage'))


#this route is to update course information in course edit page
@app.route('/Administrator_CourseEdit/Save_Edit/', methods=['POST'])
def Save_CoueseEdit():
    if request.method == 'POST':
        startDate = datetime.strptime(request.form.get('startDate'), '%Y-%m-%d')
        endDate = datetime.strptime(request.form.get('endDate'), '%Y-%m-%d')
        sql = '''
        update course
        set courseStartTime = '%s', courseEndTime = '%s'
        where courseName = '%s'
        ''' % (startDate, endDate, request.form.get('courseName'))
        database = DatabaseOperations()
        database.update(sql)
        return redirect(url_for('admin_coursespage'))


#this route is to show class information in certain course page
@app.route('/Administrator_Coursespage/<courseName>')
@login_required
def admin_coursespage_java(courseName):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    certainclass = """
    select classID, classname, courseStartTime, courseEndTime, capacity, count(distinct sid), count(distinct tid)
    from class natural join course natural join havecourse natural join teachcourse
    where coursename = '%s'
    group by classname
    """ % courseName
    
    database = DatabaseOperations()
    certainclassInfo = database.getBySql(certainclass)
    
    classlist=[]
    for i in range(len(certainclassInfo)):
        classlist.append([])
    for i in range(len(certainclassInfo)):
        classlist[i].append(certainclassInfo[i][0])
        classlist[i].append(certainclassInfo[i][1])
        classlist[i].append(certainclassInfo[i][2])
        classlist[i].append(certainclassInfo[i][3])
        classlist[i].append(certainclassInfo[i][4])
        classlist[i].append(certainclassInfo[i][5])
        classlist[i].append(certainclassInfo[i][6])
        
    return render_template('Administrator_Coursespage_Java.html', coursename = courseName, classInfo = classlist)


#this route is to delete students in certain class
@app.route('/Administrator_Classe_Java1001/<courseName>/<id>/')
@login_required
def admin_delete_class(courseName, id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    delete = """
        delete from class where classID = %d
    """ % (int(id))
    database = DatabaseOperations()
    database.update(delete)
    return redirect(url_for('admin_coursespage_java', courseName=courseName))


#this route is to show class information in class edit page
@app.route('/Administrator_Coursespage_JavaEdit/<courseName>/<className>')
@login_required
def admin_coursespageEdit_JavaEdit(courseName,className):
    if session.get('role') != 'Administrator':
        return render_template('404.html')

    certainclass = """
    select classname, courseStartTime, courseEndTime, capacity, count(distinct sid), count(distinct tid)
    from class natural join course natural join havecourse natural join teachcourse
    where className = '%s'
    group by classname
    """ % className
    
    database = DatabaseOperations()
    certainclassInfo = database.getBySql(certainclass)
    
    classlist=[]
    for i in range(len(certainclassInfo)):
        classlist.append([])
    for i in range(len(certainclassInfo)):
        classlist[i].append(certainclassInfo[i][0])
        classlist[i].append(certainclassInfo[i][1])
        classlist[i].append(certainclassInfo[i][2])
        classlist[i].append(certainclassInfo[i][3])
        classlist[i].append(certainclassInfo[i][4])
        classlist[i].append(certainclassInfo[i][5])
        
    return render_template('Administrator_Coursespage_JavaEdit.html', courseName=courseName, className=className, classInfo=classlist)


#this route is to update class information in class edit page
@app.route('/Administrator_Coursespage_JavaEdit/Save_Edit/', methods=['POST'])
def Save_coursespage_JavaEdit():
    if request.method == 'POST':
        sql = '''
        update class
        set capacity = %d
        where className = '%s'
        ''' % (int(request.form.get('capacity')), request.form.get('className'))
        database = DatabaseOperations()
        database.update(sql)
        coursename = request.form.get('coursename')
        return redirect(url_for('admin_coursespage_java', courseName=coursename))


#this route is show the teacher and students information in certain class
@app.route('/Administrator_Classe_Java1001/<className>')
@login_required
def administrator_classe_Java1001(className):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    teacher = """
    select id, name, gender, age, tlevel, phone, email
    from teacher, teachcourse, class
    where teacher.id = teachcourse.tid and teachcourse.classID = class.classID and teachcourse.courseID = class.courseID and className = '%s'
    """ % className
    
    student = """
    select id, name, gender, age, slevel, phone, email
    from student, havecourse, class
    where student.id = havecourse.sid and havecourse.classID = class.classID and havecourse.courseID = class.courseID and className = '%s'
    """ % className
    
    database = DatabaseOperations()
    teacherInfo = database.getBySql(teacher)
    studentInfo = database.getBySql(student)
    
    teacherCertainClass=[]
    for i in range(len(teacherInfo)):
        teacherCertainClass.append([])
    for i in range(len(teacherInfo)):
        teacherCertainClass[i].append(teacherInfo[i][0])
        teacherCertainClass[i].append(teacherInfo[i][1])
        teacherCertainClass[i].append(teacherInfo[i][2])
        teacherCertainClass[i].append(teacherInfo[i][3])
        teacherCertainClass[i].append(teacherInfo[i][4])
        teacherCertainClass[i].append(teacherInfo[i][5])
        teacherCertainClass[i].append(teacherInfo[i][6])
    
    studentCertainClass=[]
    for i in range(len(studentInfo)):
        studentCertainClass.append([])
    for i in range(len(studentInfo)):
        studentCertainClass[i].append(studentInfo[i][0])
        studentCertainClass[i].append(studentInfo[i][1])
        studentCertainClass[i].append(studentInfo[i][2])
        studentCertainClass[i].append(studentInfo[i][3])
        studentCertainClass[i].append(studentInfo[i][4])
        studentCertainClass[i].append(studentInfo[i][5])
        studentCertainClass[i].append(studentInfo[i][6])
    
    return render_template('Administrator_Classe_Java1001.html', classname = className, teacher = teacherCertainClass, student = studentCertainClass)


#this route is to delete students in certain class
@app.route('/Administrator_ClasseStudent_Java1001/<className>/<id>/')
@login_required
def admin_delete_classStudent(className, id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    delete = """
        delete from havecourse where sID = %d
    """ % (int(id))
    database = DatabaseOperations()
    database.update(delete)
    return redirect(url_for('administrator_classe_Java1001', className=className))


#this route is to show teacher information in teacher edit page
@app.route('/Administrator_ClassStudentEdit/<className>/<id>/')
@login_required
def admin_edit_classStudent(className, id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    student = """
        select name, gender, age, slevel, phone, email from student where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    infor = database.getBySql(student)
    name = infor[0][0]
    gender = infor[0][1]
    age = infor[0][2]
    email = infor[0][5]
    phoneNum = infor[0][4]
    level = infor[0][3]
    return render_template('Administrator_Class_StudentEdit.html', id=int(id), name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, className=className)

#this route is update student information in student edit page
@app.route('/Administrator_ClassStudentEdit/Save_Edit/<className>/<id>/', methods=['POST'])
def Save_ClassStudentEdit(className, id):
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        sql = '''
        update student
        set name = '%s', gender = '%s', age = %d, slevel = %d, email = '%s', phone = '%s'
        where id = %d
        ''' % (form.name.data, form.gender.data, int(form.age.data), int(request.form.get('level')), form.email.data, form.phoneNum.data, int(id))
        database = DatabaseOperations()
        database.update(sql)
        return redirect(url_for('administrator_classe_Java1001', className=className))


#this route is delete teacher in certain class
@app.route('/Administrator_ClasseTeacher_Java1001/<className>/<id>/')
@login_required
def admin_delete_classTeacher(className, id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    teaNum = """
        SELECT className, COUNT(DISTINCT tID)
        FROM class natural JOIN teachcourse 
        WHERE className = '%s' 
        GROUP BY className
    """ % (className)
    database = DatabaseOperations()
    infor = database.getBySql(teaNum)
    num = infor[0][1]
    if num > 1:
        delete = """
            delete from teachcourse where tID = %d
        """ % (int(id))
        database = DatabaseOperations()
        database.update(delete)
    else:
        flash('Can not delete when only one teacher in class')
        flash('You may add another teacher first')
        flash('Then you can delete')
    return redirect(url_for('administrator_classe_Java1001', className=className))


#this route is to show teacher information in teacher edit page in certain class
@app.route('/Administrator_ClassTeacherEdit/<className>/<id>/')
@login_required
def admin_edit_classTeacher(className, id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    teacher = """
        select name, gender, age, tlevel, phone, email from teacher where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    infor = database.getBySql(teacher)
    name = infor[0][0]
    gender = infor[0][1]
    age = infor[0][2]
    email = infor[0][5]
    phoneNum = infor[0][4]
    level = infor[0][3]

    return render_template('Administrator_Class_TeacherEdit.html', id=int(id), name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, className=className)

#this route is to update teacher in teacher edit page sin certain class
@app.route('/Administrator_ClassTeacherEdit/Save_Edit/<className>/<id>/', methods=['POST'])
def Save_ClassTeacherEdit(className, id):
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        sql = '''
        update teacher
        set name = '%s', gender = '%s', age = %d, tlevel = %d, email = '%s', phone = '%s'
        where id = %d
        ''' % (form.name.data, form.gender.data, int(form.age.data), int(request.form.get('level')), form.email.data, form.phoneNum.data, int(id))
        database = DatabaseOperations()
        database.update(sql)
        return redirect(url_for('administrator_classe_Java1001', className=className))


#this route is to show all student information in database
@app.route('/Administrator_Studentspage')
@login_required
def admin_studentspage():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allstudents = """
    select name, gender, age, slevel, phone, email
    from student
    limit 1000
    """ 
    
    database = DatabaseOperations()
    allstudentsInfo = database.getBySql(allstudents)    
    
    list4=[]
    for i in range(len(allstudentsInfo)):
        list4.append([])
    for i in range(len(allstudentsInfo)):
        list4[i].append(allstudentsInfo[i][0])
        list4[i].append(allstudentsInfo[i][1])
        list4[i].append(allstudentsInfo[i][2])
        list4[i].append(allstudentsInfo[i][3])
        list4[i].append(allstudentsInfo[i][4])
        list4[i].append(allstudentsInfo[i][5])
    return render_template('Administrator_Studentspage.html', message = list4)

#this route is to show all student in edit page
@app.route('/Administrator_StudentsEdit')
@login_required
def admin_studentsEdit():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allstudents = """
    select id, name, gender, age, slevel, phone, email
    from student
    limit 1000
    """ 
    
    database = DatabaseOperations()
    allstudentsInfo = database.getBySql(allstudents)    
    
    list4=[]
    for i in range(len(allstudentsInfo)):
        list4.append([])
    for i in range(len(allstudentsInfo)):
        list4[i].append(allstudentsInfo[i][0])
        list4[i].append(allstudentsInfo[i][1])
        list4[i].append(allstudentsInfo[i][2])
        list4[i].append(allstudentsInfo[i][3])
        list4[i].append(allstudentsInfo[i][4])
        list4[i].append(allstudentsInfo[i][5])
        list4[i].append(allstudentsInfo[i][6])
    return render_template('Administrator_StudentsEdit.html', message = list4)


#this route is to delete student information in edit page
@app.route('/Administrator_StudentsEdit/<id>/')
@login_required
def admin_delete_student(id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    delete = """
        delete from student where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    database.update(delete)
    return redirect(url_for('admin_studentsEdit'))


#this route is to show reture all information in student edit page
@app.route('/Administrator_StudentEdit/<id>/')
@login_required
def admin_edit_student(id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    student = """
        select name, gender, age, slevel, phone, email from student where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    infor = database.getBySql(student)
    name = infor[0][0]
    gender = infor[0][1]
    age = infor[0][2]
    email = infor[0][5]
    phoneNum = infor[0][4]
    level = infor[0][3]

    return render_template('Administrator_StudentEdit.html', id=int(id), name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level)

#this page is to update the student information in student edit page
@app.route('/Administrator_StudentEdit/Save_Edit/', methods=['POST'])
def Save_StudentEdit():
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        sql = '''
        update student
        set name = '%s', gender = '%s', age = %d, slevel = %d, email = '%s', phone = '%s'
        where id = %d
        ''' % (form.name.data, form.gender.data, int(form.age.data), int(request.form.get('level')), form.email.data, form.phoneNum.data, int(request.form.get('id')))
        database = DatabaseOperations()
        database.update(sql)
        return redirect(url_for('admin_studentsEdit'))


#this route is to show all information in teacher infor page 
@app.route('/Administrator_Teacherspage')
@login_required
def admin_teacherspage():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allteachers = """
    select name, gender, age, tlevel, phone, email
    from teacher  
    """
    
    database = DatabaseOperations()
    allteachersInfo = database.getBySql(allteachers)
    
    list3=[]
    for i in range(len(allteachersInfo)):
        list3.append([])
    for i in range(len(allteachersInfo)):
        list3[i].append(allteachersInfo[i][0])
        list3[i].append(allteachersInfo[i][1])
        list3[i].append(allteachersInfo[i][2])
        list3[i].append(allteachersInfo[i][3])
        list3[i].append(allteachersInfo[i][4])
        list3[i].append(allteachersInfo[i][5])
    return render_template('Administrator_Teacherspage.html', message = list3)

#this route is to show all information in teacher edit page
@app.route('/Administrator_TeachersEdit')
@login_required
def admin_teachersEdit():
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    
    allteachers = """
    select id, name, gender, age, tlevel, phone, email
    from teacher  
    """
    
    database = DatabaseOperations()
    allteachersInfo = database.getBySql(allteachers)
    
    list3=[]
    for i in range(len(allteachersInfo)):
        list3.append([])
    for i in range(len(allteachersInfo)):
        list3[i].append(allteachersInfo[i][0])
        list3[i].append(allteachersInfo[i][1])
        list3[i].append(allteachersInfo[i][2])
        list3[i].append(allteachersInfo[i][3])
        list3[i].append(allteachersInfo[i][4])
        list3[i].append(allteachersInfo[i][5])
        list3[i].append(allteachersInfo[i][6])
    return render_template('Administrator_TeachersEdit.html', message = list3)

#this route is to show information in certain teacher deit page
@app.route('/Administrator_TeachersEdit/<id>/')
def admin_delete_teacher(id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    delete = """
        delete from teacher where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    database.update(delete)
    return redirect(url_for('admin_teachersEdit'))

#this route is to edit teacher in certain teacher deit page
@app.route('/Administrator_TeacherEdit/<id>/')
@login_required
def admin_edit_teacher(id):
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    teacher = """
        select name, gender, age, tlevel, phone, email from teacher where id = %d
    """ % (int(id))
    database = DatabaseOperations()
    infor = database.getBySql(teacher)
    print(infor)
    name = infor[0][0]
    gender = infor[0][1]
    age = infor[0][2]
    email = infor[0][5]
    phoneNum = infor[0][4]
    level = infor[0][3]

    return render_template('Administrator_TeacherEdit.html', id=int(id), name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level)

#this route is to update teacher's information in certain teacher deit page
@app.route('/Administrator_TeacherEdit/Save_Edit/', methods=['POST'])
def Save_TeacherEdit():
    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        sql = '''
        update teacher
        set name = '%s', gender = '%s', age = %d, tlevel = %d, email = '%s', phone = '%s'
        where id = %d
        ''' % (form.name.data, form.gender.data, int(form.age.data), int(request.form.get('level')), form.email.data, form.phoneNum.data, int(request.form.get('id')))
        database = DatabaseOperations()
        database.update(sql)
        return redirect(url_for('admin_teachersEdit'))



#this route is to add a unmber into certain class
@app.route('/Administrator_Classe_Java1001Add/<className>', methods = ['GET', 'POST'])
@login_required
def administrator_classe_Java1001Add(className):
    #check role
    if session.get('role') != 'Administrator':
        return render_template('404.html')
    #initialize form and check the operation
    #if the operation is post ant the form is validate then insert a new number in current class
    form = addForm(request.form)
    if request.method == 'POST' and form.validate():
        #get the username you want to add into current class
        username = form.name.data
        database = DatabaseOperations()
        classInfo = database.getBySql("""select courseid, classid from class where classname = '%s'""" % className)
        
        #conduct following operations if user want to add a teacher
        if username[0] == "T":
            teaID = database.getBySql("""select id from teacher where username = '%s'""" % username)
            #flash back a worning if the username is not exist
            if teaID == ():
                flash("Teacher %s is not exist!"%username)
                return redirect(url_for('administrator_classe_Java1001Add', className=className))
            print(classInfo[0][0], teaID[0][0], classInfo[0][1])
            closeForeignKey = """SET FOREIGN_KEY_CHECKS=0"""
            openForeignKey = """SET FOREIGN_KEY_CHECKS=1"""
            distributeTea = """
            insert into teachcourse (courseid, tid, classid) 
            values (%d, %d, %d)
            """ % (classInfo[0][0], teaID[0][0], classInfo[0][1])
            database.insert3(closeForeignKey, distributeTea, openForeignKey)  
              
        #conduct following operations if user want to add a student
        if username[0] == "S":
            stuID = database.getBySql("""select id from student where username = '%s'""" % username)
            #flash back a warning if the username is not exist
            if stuID == ():
                flash("Student %s is not exist!"%username)
                return redirect(url_for('administrator_classe_Java1001Add', className=className))
            closeForeignKey = """SET FOREIGN_KEY_CHECKS=0"""
            openForeignKey = """SET FOREIGN_KEY_CHECKS=1"""
            distributeStu = """
            insert into havecourse (courseid, sid, classid) 
            values (%d, %d, %d)
            """ % (classInfo[0][0], stuID[0][0], classInfo[0][1])
            database.insert3(closeForeignKey, distributeStu, openForeignKey)            
        return redirect(url_for('administrator_classe_Java1001', className=className))
    #flash warning if the input is invalid
    elif request.method == 'POST':
        flash("Invalid Input!")
    return render_template('Administrator_Classe_Java1001Add.html', classname = className)




#------------------------------------------------------------------------------------------------------------------------------------------
#TEACHER

#Teacher Homepage
'''
1. Some infor about the course
2. Show teacher's personal information
3. Give the button to edit the person information
'''
@app.route('/Teacher_Homepage')
@login_required
def teacher():
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    database = DatabaseOperations()
    totalClassSQL='''
    select count(classID)
    from teachcourse
    where tid = %s
    ''' % session.get('id')
    stuNumSQL = '''
    select count(sid)
    from havecourse as H, teachcourse as T
    where H.classID = T.classID AND tid = %s
    ''' % session.get('id')
    totalClass = database.getBySql(totalClassSQL)
    stuNum = database. getBySql(stuNumSQL)
    infor = database.getInfomation(session.get('userName'))
    print(session.get('userName'))
    database.db_connect()
    name = infor[0]
    gender = infor[1]
    age = infor[2]
    email = infor[3]
    phoneNum = infor[4]
    level = infor[7]
    photo = str(infor[5], encoding ='utf-8')
    return render_template('Teacher_Homepage.html',name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, photo = photo, totalClass = totalClass[0][0], stuNum = stuNum[0][0])

#Edit Teacher's Personal Infor
'''
Change Teacher personal infor
'''
@app.route('/Teacher_HomeEditpage',  methods=['GET', 'POST'])
@login_required
def teacherEdit():
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    database = DatabaseOperations()
    infor = database.getInfomation(session.get('userName'))
    print(session.get('userName'))
    database.db_connect()
    name = infor[0]
    gender = infor[1]
    age = infor[2]
    email = infor[3]
    phoneNum = infor[4]
    preavatar = str(infor[5], encoding='utf-8')
    level = infor[7]

    form = editForm(request.form)
    if request.method == 'POST' and form.validate():
        avatarfile = request.files["image"]
        print(avatarfile)
        filename = secure_filename(avatarfile.filename)
        print(filename)
        if filename == '':
            image = preavatar
        else:
            avatarfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = url_for('uploaded_file', filename=filename)
            print(image)
        
        sql = '''
        update teacher
        set name = '%s', age = %d, email = '%s', phone = '%s', gender = '%s', avatar = '%s'
        where userName = '%s'
        ''' %(form.name.data, int(form.age.data), form.email.data, form.phoneNum.data, form.gender.data, image, session.get('userName'))
        database = DatabaseOperations()
        database.update(sql)
        return redirect('Teacher_Homepage')
    return render_template('Teacher_HomeEditpage.html',name = name, gender = gender, age = age, email =email, phoneNum = phoneNum, level = level, preavatar=preavatar)
#Teacher course infor
'''
1. Show the coming classes
2. List the Course a teacher has and give the link to each classes page
'''
@app.route('/Teacher_Coursepage')
@login_required
def teacherCourse():
    #check the role
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    
    #SQL
    #Get the coming class
    courseSQL = '''
    select CO.courseName, CL.className, CL.classID
    from teachcourse as T, class as CL, course as CO
    where T.courseID = CO.courseID AND T.classID = CL.classID AND tID = %s
    ''' % session.get('id')

    #list the classes a teacher teaches
    numberSQL = '''
    with temp as (
        select CL.classID, CL.className
        from teachcourse as T, class as CL, course as CO
        where T.courseID = CO.courseID AND T.classID = CL.classID AND tID = %s
    )
    select T.className, count(sID)
    from havecourse as HA, temp as T
    where HA.classID = T.classID
    group by T.className
    ''' % session.get('id')
    
    #Database Operations
    database = DatabaseOperations()
    courseS = database.getBySql(courseSQL)
    stuNumber = database.getBySql(numberSQL)
    course = []
    for i in range(len(courseS)):
        course.append([])
        course[i].append(courseS[i][0])
        course[i].append(courseS[i][1])
        course[i].append(courseS[i][2])
        for index in stuNumber:
            if course[i][1] == index[0]:
                course[i].append(index[1])
    return render_template('Teacher_Coursepage.html', test = course, message = course)

#Class page
'''
1. List the coming classes of one class
2. List the lecture brief
3. List all the student information
3. Give the link to see one student attendance detail
4. Give the link to see one student grade detail
'''
@app.route('/Teacher_Classpage/<classID>')
@login_required
def teacherClass(classID):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #SQL
    #Get the class name
    classNameSQL = '''
    select className
    from class
    where classid = %s
    ''' % classID
    #Get the lecture brief
    lectureDetailSQL = '''
    select lectureName, description
    from lecture
    where classid = %s
    '''  % classID
    #Get the coming classes
    comingLecSql = '''
    select lectureDate, lectureStartTime, lectureEndTime, lecturename
    from lecture
    where classID = %s
    order by lectureName
    limit 5
    ''' % classID
    #Get the student Infor
    studentSQL = '''
    select username, name, age, id
    from student, havecourse
    where sid = id AND classid = %s
    ''' % classID
    #Database Operations
    database = DatabaseOperations()
    className = database.getBySql(classNameSQL)
    lectureDetail = database.getBySql(lectureDetailSQL)
    coming = database.getBySql(comingLecSql)
    student = database.getBySql(studentSQL)
    className = database.getBySql(classNameSQL)
    return render_template('Teacher_Classpage.html', className = className,coming = coming , lectureDetail = lectureDetail, test = student, student = student, classID = classID)

#Teacher One student attendacne
'''
1. list one student all attendance
2. Give button to go to attendance edit page
'''
@app.route('/Teacher_Classpage/<classID>/attendance/<sid>')
@login_required
def teacherAttendance(classID,sid):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #SQL
    #Get student name
    stuNameSQL = '''
    select name
    from student
    where id = %s
    ''' % sid
    #Get attendacne Infor
    attendanceSQL = '''
    with temp as(
        select lectureID, lectureName, lectureDate, lectureStartTime, lectureEndTime  
        from lecture
        where classId = %s
    )
    select T.lectureID, T.lectureName, T.lectureDate, T.lectureStartTime, T.lectureEndTime, status
    from temp as T, attendance as A
    where T.lectureID = A.lectureID AND sid = %s
    ''' % (classID, sid)
    #Get Class name
    classNameSql = '''
    select className
    from class
    where classID = %s
    ''' % classID

    #Database Operations
    database = DatabaseOperations()
    stuName = database.getBySql(stuNameSQL)
    attendance = database.getBySql(attendanceSQL)
    className= database.getBySql(classNameSql)
    return render_template('Teacher_Attendancepage.html', stuName = stuName, attendance = attendance, test = attendance, sid = sid, classID = classID, className = className)

#Change students' attendance status
'''
By the date from routing Update the attendacne status
'''
@app.route('/Teacher_Classpage/<classID>/attendance/<sid>/edit/<status>/<lectureID>')
@login_required
def AttendanceEdit(classID,sid,status,lectureID):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #Check the status teacher want to change
    if status == 'P':
        status = int(1)
    elif status == 'A':
        status = int(2)
    #SQL
    #Update
    attendanceUpdate = '''
    update attendance
    set status = %d
    where lectureId = %s AND sid = %s
    ''' % (int(status), lectureID, sid)
    #Database Operations
    database = DatabaseOperations()
    database.update(attendanceUpdate)
    #Generate redirect url
    url = '/Teacher_Classpage/%s/attendance/%s/edit' % (classID, sid)
    return redirect(url) 

#Teacher attendance Edit page
'''
1. list all the attendance of one student
2. If there is no record of Present or Absent, provide two functions:
    * Change to Presnet
    * change to Absent
3. If the status is Present, allow teacher change attendance to Absent.
3. If the status is Absent, allow teacher change attendance to Present.
'''
@app.route('/Teacher_Classpage/<classID>/attendance/<sid>/edit')
@login_required
def teacherAttendanceEdit(classID,sid):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #SQL
    #Get student name
    stuNameSQL = '''
    select name
    from student
    where id = %s
    ''' % sid
    #Get the student attendance Infor
    attendanceSQL = '''
    with temp as(
        select lectureID, lectureName, lectureDate, lectureStartTime, lectureEndTime  
        from lecture
        where classId = %s
    )
    select T.lectureID, T.lectureName, T.lectureDate, T.lectureStartTime, T.lectureEndTime, status
    from temp as T, attendance as A
    where T.lectureID = A.lectureID AND sid = %s
    ''' % (classID, sid)
    #Get Class name
    classNameSql = '''
    select className
    from class
    where classID = %s
    ''' % classID

    #Database Operations
    database = DatabaseOperations()
    stuName = database.getBySql(stuNameSQL)
    attendance = database.getBySql(attendanceSQL)
    className= database.getBySql(classNameSql)
    return render_template('Teacher_AttendanceEdit.html', stuName = stuName, attendance = attendance, sid = sid,classID = classID, className = className)

#Teacher grade page
'''
Shows one student all assignmet grade
1. If the assignmet is submitted and have grade, teacher can change the grade by click the edit grade to go to edit grade page
2. Teacher can change the status of the grade by clicking edit status
3. If the Assignment haven't been submitted, teacher can not give grade.
4. If the Assignment is already have a grade which is greater than 0, teacher can not change the Status to Not Submit
'''
@app.route('/Teacher_Classpage/<classID>/grade/<sid>')
@login_required
def teacherGrade(classID, sid):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #Get Student Name
    stuNameSQL = '''
    select name
    from student
    where id = %s
    ''' % sid
    #Get Grade
    gradeSQL = '''
    with temp as(
        select lectureID, lectureName
        from lecture
        where classid = %s
    )
    select lectureName, status, assignmentGrade, T.lectureID
    from temp as T, assignment as A
    where T.lectureID = A.lectureID AND sid = %s
    ''' % (classID, sid)
    #Get Class name
    classNameSQL = '''
    select className
    from class
    where classID = %s
    ''' % classID

    database = DatabaseOperations()
    stuName = database.getBySql(stuNameSQL)
    grade = database.getBySql(gradeSQL)
    className = database.getBySql(classNameSQL)[0][0]

    return render_template('Teacher_Gradepage.html', stuName = stuName, grade = grade, classID = classID, sid = sid, className = className)

#CHANGE STATUS PAGE
'''
List all the assignemt.
1. If the Status is not published, teacher can change the status to Not submit or Submitted
2. If the status is submitted, teacher can change the status to Not submit
2. If the status is Not submit, teacher can change the status to submitted
**IMPORTANT！
If a Assignment is submitted and have a grade greater than 0, teacher can not change the status to Not Submit
'''
@app.route('/Teacher_Classpage/<classID>/grade/<sid>/status')
@login_required
def teachergradeEdit(classID,sid):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #SQL
    #Get student name
    stuNameSQL = '''
    select name
    from student
    where id = %s
    ''' % sid
    #Get the assignmet information
    gradeSQL = '''
    with temp as(
        select lectureID, lectureName
        from lecture
        where classid = %s
    )
    select lectureName, status, assignmentGrade, T.lectureID
    from temp as T, assignment as A
    where T.lectureID = A.lectureID AND sid = %s
    ''' % (classID, sid)
    #Get the class name
    classNameSQL = '''
    select className
    from class
    where classid = %s
    ''' % classID
    #Database Operations
    database = DatabaseOperations()
    stuName = database.getBySql(stuNameSQL)
    grade = database.getBySql(gradeSQL)
    className = database.getBySql(classNameSQL)
    return render_template('Teacher_Grade_StatusEdit.html', stuName = stuName, grade = grade, classID = classID, sid = sid, className = className)

#CHANGE STATUS FUNCTION
'''
Update the Assignemt Sataus by the date form routing
'''
@app.route('/Teacher_Classpage/<classID>/grade/<sid>/status/<status>/<lectureID>')
@login_required
def gradeEdit(classID,sid,status,lectureID):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #Get the status teacher want to change to.
    if status == 'NS':
        status = int(2)
    elif status == 'S':
        status = int(1)
    #SQL
    #Update
    attendanceUpdate = '''
    update assignment
    set status = %d
    where lectureId = %s AND sid = %s
    ''' % (int(status), lectureID, sid)
    #Database Operation
    database = DatabaseOperations()
    database.update(attendanceUpdate)
    #Generate the Url
    url = '/Teacher_Classpage/%s/grade/%s/status' % (classID, sid)
    return redirect(url) 

#CHANGE GRADE PAGE
'''
The grade edit page, teacher can edit one grade one time
'''
@app.route('/Teacher_Classpage/<classID>/grade/<sid>/grade/<lectureID>', methods = ['POST','GET'])
@login_required
def teacherAssigEdit(classID,sid,lectureID):
    #check if the role is correct
    if session.get('role') != 'Teacher':
        return render_template('404.html')
    #SQL
    #Get the StuName
    stuNameSQL = '''
    select name
    from student
    where id = %s
    ''' % sid
    #Get the assignment information
    gradeSQL = '''
    with temp as(
        select lectureID, lectureName
        from lecture
        where classid = %s
    )
    select lectureName, status, assignmentGrade, T.lectureID
    from temp as T, assignment as A
    where T.lectureID = A.lectureID AND sid = %s AND T.lectureID = %s
    ''' % (classID, sid, lectureID)
    #Get the class name
    classNameSQL = '''
    select className
    from class
    where classid = %s
    ''' % classID
    #Database Operation
    database = DatabaseOperations()
    stuName = database.getBySql(stuNameSQL)
    grade = database.getBySql(gradeSQL)
    form = Grade(request.form)
    className = database.getBySql(classNameSQL)
    #If the form is posted
    if request.method == 'POST':
        listA = []
        #Get the changed grade from form
        listA.append(form.grade.data)
        #SQL
        #Update the assignmet
        sql = '''
        update assignment
        set assignmentGrade = %s
        where lectureId = %s AND sid = %s
        ''' % (form.grade.data, lectureID, sid)
        database.update(sql)
        #Generate URL
        url = '/Teacher_Classpage/%s/grade/%s' % (classID,sid)
        return redirect(url)
    return render_template('Teacher_Grade_GradeEdit.html', stuName = stuName, grade = grade, classID = classID, sid = sid, className = className[0][0])


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to homepage
    return redirect('.')