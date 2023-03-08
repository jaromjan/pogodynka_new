# Optymalizacja kodu do programu pobierającego pogodę
## Zoptymalizuj kod z poprzedniego zadania z pogodą.
    1. Utwórz klasę WeatherForecast, która będzie służyła do odczytywania
        i zapisywania pliku, a także odpytywania API.
    2. Obiekt klasy WeatherForecast dodatkowo musi poprawnie implementować cztery metody:
     __setitem__
     __getitem__
     __iter__
     items
## Wykorzystaj w kodzie poniższe zapytania:
    1. weather_forecast[date] da odpowiedź na temat pogody dla podanej daty
    2. weather_forecast.items() zwróci generator tupli w formacie (data, pogoda) dla 
        już zapisanych rezultatów przy wywołaniu
    3. weather_forecast to iterator zwracający wszystkie daty, dla których znana jest pogoda