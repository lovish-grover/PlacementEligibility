-- select s.course_batch, AVG(p.problems_solved ) as problems_solved,AVG(p.latest_project_score ) as latest_project_score from students s JOIN Programming p ON p.student_id = s.student_id GROUP BY s.course_batch;

-- SELECT * FROM students s JOIN Placements pl ON pl.student_id = s.student_id where pl.placement_status = 'ready';

-- DESCRIBE softSkills;

-- SELECT ROUND(((communication + teamwork + presentation + leadership + critical_thinking + interpersonal_skills)/6), 0) AS avg_soft_skill_score,COUNT(*) AS num_students FROM SoftSkills GROUP BY avg_soft_skill_score ORDER BY avg_soft_skill_score DESC;


-- SELECT company_name, COUNT(*) AS num_placed
-- FROM Placements
-- WHERE placement_status = 'Placed'
-- GROUP BY company_name
-- ORDER BY num_placed DESC;


SELECT DATE_FORMAT(placement_date, '%Y-%m') AS month, COUNT(*) AS placements
FROM Placements
WHERE placement_status = 'Placed'
GROUP BY month
ORDER BY month DESC;

SELECT s.name, pl.internships_completed, pl.company_name
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.internships_completed >= 2 AND pl.placement_status = 'Placed';

SELECT s.city, COUNT(*) AS ready_count
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Ready'
GROUP BY s.city
ORDER BY ready_count DESC;

SELECT s.name, p.problems_solved, 
       ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2) AS avg_soft_skills
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
JOIN SoftSkills ss ON s.student_id = ss.student_id
WHERE p.problems_solved > 100 AND avg_soft_skills > 80;


SELECT s.name, pl.interview_rounds_cleared, pl.company_name
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Placed' AND pl.interview_rounds_cleared >= 3;


SELECT s.name, p.certifications_earned
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
ORDER BY p.certifications_earned DESC;
