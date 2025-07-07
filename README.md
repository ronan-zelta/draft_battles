# NFL Fantasy Points API

This API allows searching NFL players by position and name, and retrieving their fantasy points by year.

## Endpoints

### GET /health  
Returns API status.

### GET /search/{pos}?q={query}  
Search players by position and name fragment.

### GET /player/{uid}/{year}  
Get fantasy points for a player in a specific year. Returns 404 if player not found, or null if no data for that year.
