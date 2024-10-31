# Weather APIs with Django Rest Framework

## API Routes:

**All routes return JSON from the corresponding API**

Gets weather data using weatherAPI based on the location, where location can be the name of the city, ZIP code, or coordinates

```
api/weather/current/<str:location>/
```

Gets forecast data using weatherAPI

```
api/weather/forecast/<str:location>,<str:days>/
```

Gets historical data using weatherAPI (currenly doesn't work, requires paid API key :( )

```
api/weather/history/<str:location>,<str:dt>/
```

Gets daily forecast data using NWS API based on the location, where location must be coordinates lat,long.

```
api/nws/forecast/<str:latitude>,<str:longitude>/
```

Gets hourly forecast data using NWS API based on the location, where location must be coordinates lat,long.

```
api/nws/forecastHourly/<str:latitude>,<str:longitude>/
```
