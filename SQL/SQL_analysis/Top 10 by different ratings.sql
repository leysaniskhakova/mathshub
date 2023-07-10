-- 1. Топ 10 ресторанов по общему рейтингу

SELECT 
r.place_id,
ri.name,
SUM(r.rating) as overall_rating
FROM rating r
LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
GROUP BY r.place_id
ORDER BY overall_rating DESC
LIMIT 10


-- 2. Топ 10 ресторанов по рейтингу еды

SELECT 
r.place_id,
ri.name,
SUM(r.food_rating) as food_rating
FROM rating r
LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
GROUP BY r.place_id
ORDER BY food_rating DESC
LIMIT 10

						
 -- 3. Топ 10 ресторанов по рейтингу сервиса

SELECT 
r.place_id,
ri.name,
SUM(r.service_rating) as service_rating
FROM rating r
LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
GROUP BY r.place_id
ORDER BY service_rating DESC
LIMIT 10