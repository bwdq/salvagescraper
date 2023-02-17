# Salvage Scraper

Scrapes a major salvage auction site for data on vehicles and saves to a dockerised MySQL database. Used to scrape every available lot at the time, ~100k lots. MySQL database is capable of complex queries with joins in under 1s because of indexing. Wrote sample queries to find Nissan Leaf's near me. 

Ran MySQL in a docker container for portability.

Used selenium chromedriver for web automation.



### Files

DB_DDL contains the DB table definitions and sample queries

Insert_X.sql are database dumps for regenerating the database offline

CSV files contain the raw data I scraped

## Notes

Scrapes copart and saves to MySQL database
sample-search-response for https://www.copart.com/lotSearchResults/?free=true&query=*
sample-lotdetails-response for https://www.copart.com/lot/20881167/salvage-2011-nissan-armada-sv-tn-memphis

Code should first scrape VIN lotId pairs and then fill in the data for each lotId. Individual tables for make/model/color/location to save space.

See also: https://github.com/beautycodestyle/Copart
