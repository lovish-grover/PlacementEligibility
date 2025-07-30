import random
from faker import Faker
import mysql.connector

class FakeDataGenerator:
    def __init__(self, host="localhost", user="root", password="your_password", database="placement_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None
        self.cursor = None
        self.faker = Faker()

    def connect(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        print("Connected to database for inserting fake data.")

    def generate_students(self, n=50):
        student_ids = []
        for _ in range(n):
            name = self.faker.name()
            age = random.randint(18, 25)
            gender = random.choice(["Male", "Female", "Other"])
            email = self.faker.email()
            phone = self.faker.phone_number()
            enrollment_year = random.randint(2019, 2023)
            course_batch = f"Batch-{random.randint(1,5)}"
            city = self.faker.city()
            graduation_year = enrollment_year + 4

            self.cursor.execute("""
                INSERT INTO Students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year))
            student_ids.append(self.cursor.lastrowid)

        self.conn.commit()
        print(f"Inserted {n} fake students.")
        return student_ids

    def generate_programming(self, student_ids):
        for sid in student_ids:
            language = random.choice(["Python", "SQL", "Java"])
            problems_solved = random.randint(0, 200)
            assessments_completed = random.randint(0, 10)
            mini_projects = random.randint(0, 5)
            certifications_earned = random.randint(0, 3)
            latest_project_score = random.randint(0, 100)

            self.cursor.execute("""
                INSERT INTO Programming (student_id, language, problems_solved, assessments_completed,
                mini_projects, certifications_earned, latest_project_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (sid, language, problems_solved, assessments_completed,
                  mini_projects, certifications_earned, latest_project_score))

        self.conn.commit()
        print("Inserted programming data for all students.")

    def generate_soft_skills(self, student_ids):
        for sid in student_ids:
            communication = random.randint(50, 100)
            teamwork = random.randint(50, 100)
            presentation = random.randint(50, 100)
            leadership = random.randint(50, 100)
            critical_thinking = random.randint(50, 100)
            interpersonal_skills = random.randint(50, 100)

            self.cursor.execute("""
                INSERT INTO SoftSkills (student_id, communication, teamwork, presentation,
                leadership, critical_thinking, interpersonal_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (sid, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills))

        self.conn.commit()
        print("Inserted soft skills data for all students.")

    def generate_placements(self, student_ids):
        for sid in student_ids:
            mock_interview_score = random.randint(30, 100)
            internships_completed = random.randint(0, 3)
            placement_status = random.choice(["Ready", "Not Ready", "Placed"])
            company_name = self.faker.company() if placement_status == "Placed" else None
            placement_package = round(random.uniform(4, 20), 2) if placement_status == "Placed" else None
            interview_rounds_cleared = random.randint(1, 5) if placement_status == "Placed" else None
            placement_date = self.faker.date_this_year() if placement_status == "Placed" else None

            self.cursor.execute("""
                INSERT INTO Placements (student_id, mock_interview_score, internships_completed,
                placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (sid, mock_interview_score, internships_completed, placement_status,
                  company_name, placement_package, interview_rounds_cleared, placement_date))

        self.conn.commit()
        print("Inserted placement data for all students.")

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    generator = FakeDataGenerator(
        host="localhost",
        user="root",
        password="password",  
        database="placement_db"
    )
    generator.connect()
    student_ids = generator.generate_students(n=50)
    generator.generate_programming(student_ids)
    generator.generate_soft_skills(student_ids)
    generator.generate_placements(student_ids)
    generator.close()
