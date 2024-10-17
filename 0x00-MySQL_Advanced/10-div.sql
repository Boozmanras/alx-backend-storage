-- Define a function SafeDiv that returns a / b or 0 if b is 0
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- If b is 0, return 0; otherwise return the division result
    RETURN IF(b = 0, 0, a / b);
END$$

DELIMITER ;
