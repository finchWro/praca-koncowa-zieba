# 2. Charakterystyka zbioru danych

<!-- Wymagania formalne: 3–5 stron.
Elementy obowiązkowe (§3 i §10.1):
- Źródło danych z pełnym adresem URL, datą pobrania i licencją (np. CC-BY 4.0).
- Liczba obserwacji i zmiennych.
- Tabela zmiennych z opisem typów logicznych i interpretacją biznesową.
- Podstawowe statystyki opisowe.
- Analiza braków danych i wartości odstających (outlierów).
- Znane ograniczenia i specyfika zbioru.
-->

## 2.1. Źródło i licencja danych

Dane wykorzystane w niniejszej pracy pochodzą z projektu DeepMIMO [@deepmimo_website].
- **Data pobrania danych:** 2026-10-23
- **Licencja:** otwarta licencja akademicka / badawcza (Academic / Research Non-Commercial Use) z klauzulą obligatoryjnego cytowania publikacji źródłowej DeepMIMO [@Alkhateeb2019] oraz narzędzia ray-tracingowego Remcom Wireless InSite.
- **Adres źródłowy:** https://www.deepmimo.net/scenarios/v4/o1_60

## 2.2. Opis cech i zmiennych

Zbiór zawiera [N] obserwacji oraz [M] cech (zmiennych objaśniających) oraz zmienną celu `[nazwa_targetu]`.

Tabela 1. Zestawienie cech w zbiorze danych.

| Nazwa cechy | Typ danych | Opis dziedzinowy | Przykładowe wartości |
| :--- | :--- | :--- | :--- |
| `feature_1` | Numeryczny (float) | [Opis cechy 1] | 12.4, 15.8 |
| `feature_2` | Kategoryczny (str) | [Opis cechy 2] | A, B, C |
| `target`    | Binarny (int)      | Zmienna celu (0/1)   | 0, 1 |

## 2.3. Statystyki opisowe i jakość danych

[Krótkie omówienie rozkładów zmiennych, statystyk pozycyjnych i miar rozproszenia...]

## 2.4. Braki danych i wartości odstające

[Analiza braków danych (udział procentowy, mechanizm MCAR/MAR/MNAR) oraz strategie detekcji anomalii/outlierów...]

## 2.5. Ograniczenia zbioru danych

[Jawne wymienienie ograniczeń zbioru, np. specyfika próbki, reprezentatywność, błąd pomiarowy...]

\newpage
