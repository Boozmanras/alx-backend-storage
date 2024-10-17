-- This procedure computes and stores the average weighted score for a given user

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE total_score FLOAT;

    -- Calculate total weight for all projects
    SELECT SUM(p.weight)
    INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Calculate total weighted score for the user
    SELECT SUM(c.score * p.weight)
    INTO total_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Update the user's average score
    UPDATE users
    SET average_score = total_score / total_weight
    WHERE id = user_id;
END //

DELIMITER ;
