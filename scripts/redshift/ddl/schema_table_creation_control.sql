create schema control;

create table control.trips_load (hashid varchar, datetime TIMESTAMP WITHOUT TIME ZONE, comments varchar) DISTSTYLE ALL;