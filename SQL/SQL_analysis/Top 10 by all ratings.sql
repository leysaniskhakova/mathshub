-- 4. Топ 10 ресторанов по всем трем рейтингам

CREATE VIEW restaurants_top_10 AS 

WITH top_rest AS (
SELECT place_id, name
FROM (
		SELECT 
		r.place_id,
		ri.name,
		SUM(r.rating) as overall_rating
		FROM rating r
		LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
		GROUP BY r.place_id
		ORDER BY overall_rating DESC
		LIMIT 15
		)
INTERSECT
SELECT place_id, name
FROM (
		SELECT 
		r.place_id,
		ri.name,
		SUM(r.food_rating) as food_rating
		FROM rating r
		LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
		GROUP BY r.place_id
		ORDER BY food_rating DESC
		LIMIT 15
		)
INTERSECT
SELECT place_id, name
FROM (
		SELECT 
		r.place_id,
		ri.name,
		SUM(r.service_rating) as service_rating
		FROM rating r
		LEFT JOIN restaurant_info ri ON r.place_id = ri.place_id
		GROUP BY r.place_id
		ORDER BY service_rating DESC
		LIMIT 15
		)
)

SELECT 
ts.place_id, ts.name,
SUM(r.rating) as overall_rating,
SUM(r.food_rating) as food_rating,
SUM(r.service_rating) as service_rating
FROM top_rest ts
LEFT JOIN rating r ON ts.place_id = r.place_id
GROUP BY ts.place_id
ORDER BY overall_rating + food_rating + service_rating DESC
LIMIT 10