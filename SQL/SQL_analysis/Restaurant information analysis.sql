-- Количество ресторанов
SELECT COUNT(place_id) AS count_rest
FROM restaurant_info

-- Ценовой сегмент
SELECT 
price,
COUNT(price) AS count_rest
FROM restaurant_info ri
GROUP BY price 
ORDER BY count_rest DESC 

-- Кухня ресторанов
SELECT
rc.r_cuisine AS cuisine,
COUNT(rc.r_cuisine) AS count_rest
FROM restaurant_info ri 
LEFT JOIN restaurant_cuisine rc 
ON ri.place_id = rc.place_id
GROUP BY cuisine
ORDER BY count_rest DESC


-- Алкоголь
SELECT 
alcohol,
COUNT(alcohol) AS count_rest
FROM restaurant_info
GROUP BY alcohol
ORDER BY count_rest DESC

-- Среднее, максимальное и минимальное количество способов оплаты
SELECT
ROUND(AVG(count_payment)) AS avg_count_payment,
MAX(count_payment) AS max_count_payment,
MIN(count_payment) AS min_count_payment
FROM (
		SELECT 
		ri.place_id,
		COUNT(rp.r_payment) OVER (PARTITION BY rp.place_id) AS count_payment
		FROM restaurant_info ri
		LEFT JOIN  restaurant_payment rp ON rp.place_id = ri.place_id
		ORDER BY count_payment DESC
	  )
WHERE count_payment > 0

-- Способы оплаты это 
SELECT payment
FROM (
		SELECT 
		ri.place_id,
		rp.r_payment AS payment,
		COUNT(rp.r_payment) OVER (PARTITION BY rp.place_id) AS count_payment
		FROM restaurant_info ri
		LEFT JOIN  restaurant_payment rp ON rp.place_id = ri.place_id
		ORDER BY count_payment DESC
	  )
WHERE count_payment = 5
GROUP BY payment


-- Единственный способ оплаты это
SELECT payment
FROM (
		SELECT 
		ri.place_id,
		rp.r_payment AS payment,
		COUNT(rp.r_payment) OVER (PARTITION BY rp.place_id) AS count_payment
		FROM restaurant_info ri
		LEFT JOIN  restaurant_payment rp ON rp.place_id = ri.place_id
		ORDER BY count_payment DESC
	  )
WHERE count_payment = 1
GROUP BY payment