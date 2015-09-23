# censusdata

#### Run
First, set `DATABASE_FILE` in `app.cfg` to be the path to your census-data.db file. If you have Flask installed, you can then run `python app.py` to start the server; it will start on `localhost:5000` by default. The code should work well with any sqlite file as long as the `VARIABLE` parameter is set to a column that actually exists and is numeric.

#### Note
The first 16000 lines of census-data.db appear to have null values for every column. I decided to just filter them out when I return the results. Depending on the use case, a better option could be to clean the table only once before using it with this script.
