-- Create a view to show students with a score under 80 and no last meeting or last meeting over 1 month ago
CREATE VIEW need_meeting AS
SELECT name 
FROM students 
WHERE score < 80 
AND (last_meeting IS NULL OR last_meeting < CURDATE() - INTERVAL 1 MONTH);
