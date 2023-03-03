SELECT reg.region, 
       trunc(date_trunc('week', trp.datetime)) AS week_start_date, 
       AVG(trp.count_trips) AS weekly_avg_trips
FROM trips.facttrips trp
left join trips.dimregions reg on reg.cdregion = trp.cdregion
GROUP BY reg.region, week_start_date
ORDER BY reg.region, week_start_date;