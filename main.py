import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),  
        database=os.getenv("DB_NAME")
    )


def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def main():
    st.set_page_config(page_title="Placement Eligibility App", layout="wide")
    st.title("Placement Eligibility Application")

    tab1, tab2 = st.tabs(["Eligibility Filter", "Insights Dashboard"])

    with tab1:
        st.header("Filter Eligible Students")
        st.sidebar.header("Filter Criteria")
        problems_solved = st.sidebar.slider("Minimum Problems Solved", 0, 200, 50)
        soft_skill_score = st.sidebar.slider("Minimum Soft Skill Avg", 0, 100, 75)
        placement_status = st.sidebar.selectbox("Placement Status", ["Any", "Ready", "Not Ready", "Placed"])
        def fetch_eligible_students():
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT s.student_id, s.name, s.email, s.phone, s.course_batch,
                       p.language, p.problems_solved, ss.communication, ss.teamwork, 
                       pl.placement_status, pl.company_name, pl.placement_package
                FROM Students s
                JOIN Programming p ON s.student_id = p.student_id
                JOIN SoftSkills ss ON s.student_id = ss.student_id
                JOIN Placements pl ON s.student_id = pl.student_id
                WHERE 1 = 1
            """
            values = []

            if problems_solved:
                query += " AND p.problems_solved >= %s"
                values.append(problems_solved)

            if soft_skill_score:
                query += " AND ((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6) >= %s"
                values.append(soft_skill_score)

            if placement_status != "Any":
                query += " AND pl.placement_status = %s"
                values.append(placement_status)

            cursor.execute(query, tuple(values))
            result = cursor.fetchall()
            conn.close()
            return pd.DataFrame(result)

        if st.sidebar.button("Find Eligible Students"):
            df = fetch_eligible_students()
            if not df.empty:
                st.success(f"{len(df)} students found.")
                st.dataframe(df)
            else:
                st.warning("No eligible students found.")

    with tab2:
        st.header("Placement & Performance Insights")

        st.subheader("1. Average Programming Performance per Batch")
        df1 = run_query("""
            SELECT s.course_batch, 
                   AVG(p.problems_solved) AS avg_problems_solved,
                   AVG(p.latest_project_score) AS avg_project_score
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            GROUP BY s.course_batch;
        """)
        st.plotly_chart(px.bar(df1, x="course_batch", y="avg_problems_solved", title="Avg Problems Solved by Batch"))

        st.subheader("2. Top 5 Students Ready for Placement")
        df2 = run_query("""
            SELECT s.name, p.latest_project_score, pl.mock_interview_score
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Ready'
            ORDER BY pl.mock_interview_score + p.latest_project_score DESC
            LIMIT 5;
        """)
        st.dataframe(df2)

        st.subheader("3. Soft Skills Distribution")
        df3 = run_query("""
            SELECT
                ROUND(((communication + teamwork + presentation + leadership + critical_thinking + interpersonal_skills)/6), 0) AS avg_soft_skill_score,
                COUNT(*) AS num_students
            FROM SoftSkills
            GROUP BY avg_soft_skill_score
            ORDER BY avg_soft_skill_score DESC;
        """)
        st.plotly_chart(px.bar(df3, x="avg_soft_skill_score", y="num_students", title="Avg Soft Skills Distribution"))

        st.subheader("4. Number of Students Placed per Company")
        df4 = run_query("""
            SELECT company_name, COUNT(*) AS num_placed
            FROM Placements
            WHERE placement_status = 'Placed'
            GROUP BY company_name
            ORDER BY num_placed DESC;
        """)
        st.plotly_chart(px.bar(df4, x="company_name", y="num_placed", title="Placements per Company"))

        st.subheader("5. Monthly Placement Trends")
        df5 = run_query("""
            SELECT DATE_FORMAT(placement_date, '%Y-%m') AS month, COUNT(*) AS placements
            FROM Placements
            WHERE placement_status = 'Placed'
            GROUP BY month
            ORDER BY month DESC;
        """)
        st.plotly_chart(px.line(df5, x="month", y="placements", title="Monthly Placement Count"))

        st.subheader("6. Students with 2+ Internships and Placed")
        df6 = run_query("""
            SELECT s.name, pl.internships_completed, pl.company_name
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.internships_completed >= 2 AND pl.placement_status = 'Placed';
        """)
        st.dataframe(df6)

        st.subheader("7. City-wise Placement Readiness")
        df7 = run_query("""
            SELECT s.city, COUNT(*) AS ready_count
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Ready'
            GROUP BY s.city
            ORDER BY ready_count DESC;
        """)
        st.plotly_chart(px.bar(df7, x="city", y="ready_count", title="City-wise Ready Students"))

        st.subheader("8. Students with High Programming & Soft Skills")
        df8 = run_query("""
            SELECT s.name, p.problems_solved, 
                ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2) AS avg_soft_skills
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            WHERE p.problems_solved > 100 AND ((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6) > 80;
        """)
        st.dataframe(df8)

        st.subheader("9. Students Who Cleared All Interview Rounds")
        df9 = run_query("""
            SELECT s.name, pl.interview_rounds_cleared, pl.company_name
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Placed' AND pl.interview_rounds_cleared >= 3;
        """)
        st.dataframe(df9)

        st.subheader("10. Certification Count per Student")
        df10 = run_query("""
            SELECT s.name, p.certifications_earned
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            ORDER BY p.certifications_earned DESC;
        """)
        st.plotly_chart(px.bar(df10, x="name", y="certifications_earned", title="Certifications per Student"))

if __name__ == "__main__":
    main()
