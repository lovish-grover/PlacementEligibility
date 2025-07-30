import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

class MySQLDatabaseInitializer:
    def __init__(self, host="localhost", user="root", password="your_password", database="placement_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.db_name = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"]
            )
            self.cursor = self.conn.cursor()
            self.create_database()
            self.conn.database = self.db_name
            print(f"Connected to MySQL database: {self.db_name}")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            print(f"Database '{self.db_name}' created or already exists.")
        except mysql.connector.Error as err:
            print(f"Failed to create database: {err}")
            exit(1)

    def create_tables(self):
        TABLES = {}

        TABLES['Students'] = (
            """
            CREATE TABLE IF NOT EXISTS Students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(20),
                email VARCHAR(100),
                phone VARCHAR(50),
                enrollment_year INT,
                course_batch VARCHAR(50),
                city VARCHAR(100),
                graduation_year INT
            )
            """
        )

        TABLES['Programming'] = (
            """
            CREATE TABLE IF NOT EXISTS Programming (
                programming_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                language VARCHAR(50),
                problems_solved INT,
                assessments_completed INT,
                mini_projects INT,
                certifications_earned INT,
                latest_project_score INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
            """
        )

        TABLES['SoftSkills'] = (
            """
            CREATE TABLE IF NOT EXISTS SoftSkills (
                soft_skill_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                communication INT,
                teamwork INT,
                presentation INT,
                leadership INT,
                critical_thinking INT,
                interpersonal_skills INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
            """
        )

        TABLES['Placements'] = (
            """
            CREATE TABLE IF NOT EXISTS Placements (
                placement_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                mock_interview_score INT,
                internships_completed INT,
                placement_status VARCHAR(50),
                company_name VARCHAR(100),
                placement_package FLOAT,
                interview_rounds_cleared INT,
                placement_date DATE,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
            """
        )

        for table_name, ddl in TABLES.items():
            try:
                print(f"Creating table {table_name}...")
                self.cursor.execute(ddl)
                print(f"Table {table_name} created successfully.")
            except mysql.connector.Error as err:
                print(f"Error creating table {table_name}: {err}")

        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("MySQL connection closed.")

if __name__ == "__main__":
    db = MySQLDatabaseInitializer(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),  
        database=os.getenv("DB_NAME")
    )
    db.connect()
    db.create_tables()
    db.close()
