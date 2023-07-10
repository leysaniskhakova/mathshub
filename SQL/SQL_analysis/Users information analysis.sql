--Количество пользователей
SELECT COUNT(user_id)
FROM consumer_info

-- Препочитаемая кухня пользователей
SELECT
cc.u_cuisine AS cuisine,
COUNT(ci.user_id) AS count_user
FROM consumer_info ci
LEFT JOIN сonsumer_cuisine cc 
ON cc.user_id = ci.user_id
GROUP BY cc.u_cuisine
ORDER BY count_user DESC

-- Бюджет (доход) пользователей
SELECT 
budget,
COUNT(budget) AS count_us
FROM consumer_info
GROUP BY budget 
ORDER BY count_us DESC

-- Употрбеление алкоголя
SELECT 
drink_level,
COUNT(drink_level) AS count_us
FROM consumer_info
GROUP BY drink_level 
ORDER BY count_us DESC

-- Способ оплаты пользователей в ресторанах
SELECT
cp.u_payment AS payment,
COUNT(ci.user_id) AS count_user
FROM consumer_info ci
LEFT JOIN consumer_payment cp 
ON cp.user_id = ci.user_id
GROUP BY payment
ORDER BY count_user DESC