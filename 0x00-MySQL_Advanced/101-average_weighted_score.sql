-- This procedure computes and stores the average weighted score for all users

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE u_id INT;
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN user_cursor;

    read_loop: LOOP
        FETCH user_cursor INTO u_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Call the procedure to compute the average weighted score for each user
        CALL ComputeAverageWeightedScoreForUser(u_id);
    END LOOP;

    CLOSE user_cursor;
END //

DELIMITER ;
