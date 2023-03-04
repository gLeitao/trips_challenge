select distinct reg.region
FROM trips.facttrips trp
left join trips.dimregions reg on reg.cdregion = trp.cdregion 
left join trips.dimdatasources dts on dts.cddatasource = trp.cddatasource  and 
                                      lower(dts.datasource) = 'cheap_mobile'