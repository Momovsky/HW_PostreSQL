import psycopg2 as pg


def create_db():
    cur.execute('create table if not exists Student(id serial primary key, name varchar(100) not null, gpa numeric(10,2), birth timestamptz);')
    cur.execute('create table if not exists Courses(id serial primary key, name varchar(100) not null);')
    cur.execute('create table if not exists Student_Courses(id serial primary key, student_id integer references student(id), course_id integer references courses(id));')
    conn.commit()

def get_students(course_id): # возвращает студентов определенного курса
    cur.execute('''
            select c.name, s.id, s.name, s.gpa, s.birth from student_courses sc
            join student s on s.id = sc.student_id
            join courses c on c.id = sc.course_id
            where c.id = (%s);
        ''', (course_id,))
    return cur.fetchall()

def add_students(course_id, students):
    for student in students:
        cur.execute('insert into Student(name, gpa, birth) values (%s, %s, %s);', (student['name'], student['gpa'], student['birth']))
        cur.execute('select s.id from student s where s.name = %s and s.gpa = %s and s.birth = %s;', (student['name'], student['gpa'], student['birth']))
        id = cur.fetchall()
        cur.execute('insert into student_courses(student_id, course_id) values (%s, %s);', (id[0][0], course_id))


def add_student(student):
    cur.execute('insert into Student(name, gpa, birth) values (%s, %s, %s);', (student['name'], student['gpa'], student['birth']))

def get_student(student_id):
    cur.execute('select * from Student where id=(%s);', (student_id,))
    return cur.fetchall()

#пример оформления студента/списка студентов:
# list = [{
#     'name': 'Ivan',
#     'gpa': 4.81,
#     'birth': '2012-09-16 02:01:36.399357+03'
# },
# {
#     'name': 'Slava',
#     'gpa': 7.35,
#     'birth': '2020-09-16 02:01:36.399357+03'
# },
# {
#     'name': 'Igor',
#     'gpa': 2.35,
#     'birth': '2000-01-16 02:01:36.399357+03'
# }]

#Обязательная конструкция перед выполнением любых прочих действий с таблицами:
with pg.connect(database='hw_db_postgres', user='hw', password='511213', host='localhost', port=5432) as conn:
    cur = conn.cursor()

