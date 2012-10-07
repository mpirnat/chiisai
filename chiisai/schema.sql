drop table if exists urls;
create table urls (
    id integer primary key autoincrement,
    alias text unique not null,
    url text not null,
    created text not null, -- ISO8601 date string: "YYYY-MM-DD HH:MM:SS.SSS"
    hits integer
);
