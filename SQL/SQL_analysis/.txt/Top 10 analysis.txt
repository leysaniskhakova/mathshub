-- Рестораны в топе с кухнейб ценовой категорией и наличием алкоголя
SELECT
rt.name,
rc.r_cuisine AS cuisine,
ri.price, ri.alcohol
FROM restaurants_top_10 rt
LEFT JOIN restaurant_cuisine rc ON rc.place_id = rt.place_id
LEFT JOIN restaurant_info ri ON ri.place_id = rt.place_id
GROUP BY rt.name 
ORDER BY rt.overall_rating + rt.food_rating + rt.service_rating DESC

-- Кухни ресторанов в топе
SELECT *
FROM (
	SELECT 
	rc.r_cuisine AS cuisine,
	COUNT(rt.place_id) OVER (PARTITION BY r_cuisine) AS count_top_rest
	FROM restaurants_top_10 rt 
	LEFT JOIN restaurant_cuisine rc ON rc.place_id = rt.place_id
	)
GROUP BY cuisine
ORDER BY count_top_rest DESC

-- Ценовой сегмент ресторанов в топе
SELECT
ri.price, 
COUNT(ri.place_id) AS count_top_rest 
FROM restaurants_top_10 rt
LEFT JOIN restaurant_info ri ON ri.place_id = rt.place_id 
GROUP BY ri.price
ORDER BY count_top_rest DESC

-- Продажа алкоголя в рестаранах в топе
SELECT
ri.alcohol, 
COUNT(ri.place_id) AS count_top_rest 
FROM restaurants_top_10 rt
LEFT JOIN restaurant_info ri ON ri.place_id = rt.place_id 
GROUP BY ri.alcohol
ORDER BY count_top_rest DESC


-- Количество способа оплат в рестаранах в топе
SELECT 
rt.name,
COUNT(rp.r_payment) AS count_payment
FROM restaurants_top_10 rt
LEFT JOIN  restaurant_payment rp ON rp.place_id = rt.place_id
GROUP BY rt.name 
ORDER BY rt.overall_rating + rt.food_rating + rt.service_rating DESC
