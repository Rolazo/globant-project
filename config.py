SECRET_KEY = 'tfLJHPIkyXuyQRA2t6L3Qij5o2znlP2s'

# query1 = '''
# SELECT d.department, j.job, 
# SUM(CASE WHEN strftime('%m', hire_datetime) IN ('01','02','03') THEN 1 ELSE 0 END) AS Q1, 
# SUM(CASE WHEN strftime('%m', hire_datetime) IN ('04','05','06') THEN 1 ELSE 0 END) AS Q2, 
# SUM(CASE WHEN strftime('%m', hire_datetime) IN ('07','08','09') THEN 1 ELSE 0 END) AS Q3, 
# SUM(CASE WHEN strftime('%m', hire_datetime) IN ('10','11','12') THEN 1 ELSE 0 END) AS Q4 
# FROM hired_employees AS he INNER JOIN departments AS d ON he.department_id = d.id INNER JOIN jobs AS j ON he.job_id = j.id 
# WHERE strftime('%Y', hire_datetime) = '2021' 
# GROUP BY d.department, j.job ORDER BY d.department, j.job
# '''

# query2 = '''
# SELECT department_id, departments.department, 
# COUNT(*) AS hired 
# FROM hired_employees JOIN departments ON hired_employees.department_id = departments.id 
# WHERE department_id IN ( SELECT department_id FROM departments ) 
# GROUP BY department_id HAVING COUNT(*) > 
# ( SELECT AVG(hired) 
# FROM ( SELECT department_id, COUNT(*) AS hired 
# FROM hired_employees WHERE department_id IN ( SELECT department_id FROM departments ) 
# GROUP BY department_id ) AS t ) 
# ORDER BY hired DESC
# '''