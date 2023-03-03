create schema trips;

create table trips.dimregions (cdregion varchar, region varchar) DISTSTYLE ALL;

create table trips.dimdatasources (cddatasource varchar, datasource varchar) DISTSTYLE ALL;

create table trips.facttrips (cdregion varchar, 
                              cddatasource varchar, 
                              datetime TIMESTAMP WITHOUT TIME ZONE, 
                              count_trips int) 
DISTKEY (cdregion)
SORTKEY (cdregion, cddatasource) ;