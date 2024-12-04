-- 02_insert_mock_data.sql

-- Insert mock users
INSERT INTO users (username, email, password_hash, full_name)
VALUES 
('john_doe', 'john@example.com', 'hashed_password', 'John Doe'),
('jane_smith', 'jane@example.com', 'hashed_password', 'Jane Smith');

-- Insert categories (Mathematics --> Calculus --> Calculus for CS students)
INSERT INTO categories (name, parent_id, path)
VALUES 
('Mathematics', NULL, '/Mathematics'),
('Calculus', 1, '/Mathematics/Calculus'),
('Calculus for CS students', 2, '/Mathematics/Calculus/Calculus for CS students');

-- Insert target audiences
INSERT INTO target_audiences (name)
VALUES 
('CS students'),
('Mechanical Engineers');

-- Insert tutoring services
INSERT INTO tutoring_services (user_id, category_id, title, description, price)
VALUES 
(1, 3, 'CS Calculus Tutoring', 'Offering specialized calculus tutoring for CS students.', 50.00),
(2, 2, 'Advanced Calculus Tutoring', 'In-depth tutoring for calculus enthusiasts.', 40.00);


-- Insert service audiences
INSERT INTO service_audiences (tutoring_service_id, target_audience_id)
VALUES 
(1, 1),  -- Service 1 is for CS students
(2, 2);  -- Service 2 is for Mechanical Engineers
