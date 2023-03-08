import os
import requests
import csv
import datetime


class WeatherForecast:
    def __init__(self, searched_date):
        self.plik = 'opady.csv'
        self.start_iter = -1
        self.zaw = {}
        self.lista = []
        self.searched_date = searched_date
        self.opad = float()
        self.wynik = []

    def __str__(self):
        kom = ''
        if self.opad is None:
            kom = 'Brak mozliwosci pobrania danych'
        elif self.opad == 0.0:
            kom = 'Nie bedzie padac'
        elif self.opad > 0.0:
            kom = 'Bedzie padac'
        else:
            self.kom = 'Nie wiem'
        return f'W dniu: {self.searched_date}  {kom} - przewidywany opad: {self.opad}'

    def odczytaj_plik(self):
        if not os.path.exists(self.plik):
            fc = open(self.plik, 'w')
            fc.close()
        with open(self.plik, 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            for line in reader:
                self.zaw[line[0]] = line[1]
                self.lista.append(line)
            return self.zaw, self.lista

    def pobierz_api(self):
        url = f'https://api.open-meteo.com/v1/forecast?latitude={50.23}&longitude={18.66}&hourly=rain&' \
              f'daily=rain_sum&timezone=Europe%2FLondon&start_date={self.searched_date}&end_date={self.searched_date}'
        resp = requests.get(url)
        dane = resp.json()
        status = str(resp.status_code)[0]+str(resp.status_code)[1]
        if status != '20':
            print('Brak danych archiwalnych i bledna odpowiedz serwera')
            quit()
        else:
            self.opad = float(dane['daily']['rain_sum'][0])
            return self.opad

    def dopisz(self):
        self.wynik = [str(self.searched_date), self.opad]
        with open(self.plik, 'a', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
            writer.writerow(self.wynik)

    def items(self):
        for n in self.zaw:
            x = tuple([n, self.zaw[n]])
            yield x

    def __getitem__(self, item):
        self.opad = self.zaw.get(item)
        return self.opad

    def __setitem__(self, k, v):
        self.zaw[k] = v

    def __iter__(self):
        for g in self.lista:
            yield g


# Pobieramy wartosc daty i sprawdzamy poprawnosc
data_in = input("Podaj date w formacie 'YYYY-MM-DD' lub pusta(zostanie pobrana jutrzejsza): ")
if data_in == '':
    s_date = datetime.date.today() + datetime.timedelta(days=1)
else:
    try:
        data_in = data_in.split(sep='-')
        s_date = datetime.date(int(data_in[0]), int(data_in[1]), int(data_in[2]))
    except Exception as e:
        print(f'Błedna data: {e} - wczytuję datę jutrzejsza')
        s_date = datetime.date.today() + datetime.timedelta(days=1)

print('Zwracamy odpowiedź na temat pogody dla podanej daty:')
weather_forecast = WeatherForecast(str(s_date))
# pobieramy dane z pliku
weather_forecast.odczytaj_plik()
# testujemy metode __setitem__ - właczyc na potrzeby testu
# weather_forecast.__setitem__(str(s_date), 2.1)
# weryfikujemy czy mamy juz dane w pliku jeśli nie mamy pobieramy i dopisujemy do pliku
if weather_forecast.__getitem__(str(s_date)) is not None:
    print(weather_forecast)
else:
    if weather_forecast.pobierz_api() is not None:
        weather_forecast.dopisz()
        print(weather_forecast)
    else:
        print('Blad przy wywołaniu API')
print('Lista tupli w formacie (data, pogoda) dla już zapisanych rezultatów')
for z in weather_forecast.items():
    print(z)
print('Zwracamy wszystkie daty, dla których znana jest pogoda')
for n in weather_forecast:
    print(n[0])
