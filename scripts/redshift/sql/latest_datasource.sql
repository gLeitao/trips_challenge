with commun_regions as(
  SELECT 
    reg.cdregion, 
    reg.region, 
    count(*) as row_count 
  FROM 
    trips.facttrips trp 
    left join trips.dimregions reg on reg.cdregion = trp.cdregion 
  group by 
    reg.cdregion, 
    reg.region 
  order by 
    row_count desc 
  limit 
    2
) 
select 
  dts.datasource, 
  max(trp.datetime) as datetime 
FROM 
  trips.facttrips trp 
  left join trips.dimdatasources dts on dts.cddatasource = trp.cddatasource 
  inner join commun_regions cr on cr.cdregion = trp.cdregion 
group by 
  dts.datasource 
order by 
  datetime desc 
limit 
  1
