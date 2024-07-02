import os  # Import the os module to use getenv

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Database configuration
conf = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy to use PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"]=f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}:5432/postgres"
db = SQLAlchemy(app)

# Define the Student table model
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

# Route for home
@app.route("/home",methods=["GET"])
def hello():
  return "Welcome to my first Flask Server",200

# Route to get all students
@app.route("/student",methods=["GET"])
def student_list():
  # Example data
  students=[{"name":"Sam","email":"sam@gmail.com"},{"name":"Delilah","email":"delilah@gmail.com"}]
  all_students=[]
  list_students=Student.query.all() # Retrieve all students from the database
  for student in list_students:
    print(vars(student))
    all_students.append({'id':student.id,'name':student.name,'email':student.email})
  return jsonify(all_students),200

# Route to add a new student
@app.route("/student", methods=["POST"])
def add_student():
    # VALIDATION
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'}), 400
    body = request.get_json()

    # Handle single student addition
    if isinstance(body, dict):  # Check if body is a dictionary
        name = body.get('name')
        email = body.get('email')

        # Check if required fields are present
        if not name or not email:
            return jsonify({'message': "Email or name missing"}), 400
        
        # Check if student with the same email already exists
        exist_student = Student.query.filter_by(email=email).first()
        if exist_student:
            return jsonify({'message': f"Student with email {email} already exists", 'data': {
                'name': exist_student.name,
                'email': exist_student.email
            }}), 400

        # Create a new Student object and add it to the database
        st = Student(name=name, email=email)
        db.session.add(st)
        db.session.commit()
        return jsonify({'message': "Student Added"}), 200

    # Handle batch addition or unexpected format
    elif isinstance(body, list):  # Check if body is a list
        added_students = []
        for student_data in body:
            name = student_data.get('name')
            email = student_data.get('email')
            
            # Check if required fields are present for each student in the list
            if not name or not email:
                return jsonify({'message': "Email or name missing in one of the students"}), 400
 
            # Check if student with the same email already exists before adding
            exist_student = Student.query.filter_by(email=email).first()
            if exist_student:
                continue  # Skip adding if student already exists

            # Create a new Student object and add it to the database
            st = Student(name=name, email=email)
            db.session.add(st)
            added_students.append({'name': name, 'email': email})

        # Commit all changes to the database
        db.session.commit()
        return jsonify({'message': "Students Added", 'added_students': added_students}), 200
    else:
        # Return an error message if the JSON format is invalid
        return jsonify({'message': "Invalid JSON format"}), 400

# Route to update an existing student
@app.route("/student",methods=["PUT"])
def update_student():
  # Validate and process request body
  body=request.get_json()
  id=body.get("id")
  name=body.get('name')
  email=body.get('email')

  if not id:
    return request({'message':"Student id required"}),400
  
  # Retrieve student from database
  exist_student=Student.query.get(id)

  # Update student attributes if provided
  if name:
    exist_student.name=name
  if email:
    exist_student.email=email
  
  # Commit changes to the database
  db.session.commit()
  return jsonify({'message': "Student updated", 'student': {
        'name': exist_student.name,
        'email': exist_student.email
    }}), 200

# Route to delete a student by id
@app.route("/student", methods = ["DELETE"])
def delete_student():
  # Retrieve student id from request body
  body = request.get_json()
  id = body.get('id')

  if not id:
    return jsonify({'message':'Id required to delete student'}),400
  
  # Retrieve student from database
  exist_student=Student.query.get(id)
  if not exist_student:
    return jsonify({'message':'Student to delete does not exist'}),400
  
  # Delete student from database
  db.session.delete(exist_student)
  db.session.commit()

  return jsonify({'message': 'Student deleted successfully'}), 204

# CRUD, CREATE, READ , UPDATE , DELETE

# DYNAMIC URLS

# Route to get student by id
@app.route("/student/<int:id>",methods=["GET"])
def get_student_by_id(id):
  # Retrieve student from database by id
  student=Student.query.get(id)

  if not student:
    return jsonify({'message':f'Student with id {id} does not exist'}),400
  
  return jsonify({  'name':student.name,'email':student.email}),200

# Run the Flask application8
if __name__=="__main__":
  app.run(debug=True,port=9000)