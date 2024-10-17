-- This script shows and computes the average weighted score for all users

SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

-- Compute the average weighted score for all users
CALL ComputeAverageWeightedScoreForUsers();

SELECT "--";
SELECT * FROM users;
