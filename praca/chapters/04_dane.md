# 2. Charakterystyka zbioru danych

<!-- Wymagania formalne: 3–5 stron.
Elementy obowiązkowe (§3 i §10.1):
- Źródło danych z pełnym adresem URL, datą pobrania i licencją (np. CC-BY 4.0).
- Liczba obserwacji i zmiennych.
- Tabela zmiennych z opisem typów logicznych i interpretacją biznesową.
- Podstawowe statystyki opisowe
- Analiza braków danych i wartości odstających (outlierów).
- Znane ograniczenia i specyfika zbioru.
-->

## 2.1. Źródło i licencja danych

Dane wykorzystane w niniejszej pracy pochodzą z projektu DeepMIMO [@deepmimo_website].
- **Data pobrania danych:** 2026-10-23
- **Licencja:** otwarta licencja akademicka / badawcza (Academic / Research Non-Commercial Use) z klauzulą obligatoryjnego cytowania publikacji źródłowej DeepMIMO [@Alkhateeb2019] oraz narzędzia ray-tracingowego Remcom Wireless InSite.
- **Adres źródłowy:** https://www.deepmimo.net/scenarios/v4/o1_60

### 2.1.1. Opis symulacji ray-tracingowej w Remcom Wireless InSite

Dane pochodzą z symulacji przeprowadzonej za pomocą oprogramowania do śledzenia promieni (ang. *ray tracing*) Remcom Wireless InSite, na podstawie trójwymiarowego modelu środowiskowego przedstawiającego skrzyżowanie ulic o geometrii kanionu miejskiego (ang. *urban canyon*). Scenę przygotowano w środowisku CAD (ang. *Computer-Aided Design*), a właściwości elektromagnetyczne budynków zdefiniowano zgodnie z zaleceniami ITU-R (ang. *International Telecommunication Union – Radiocommunication Sector*). W analizowanym środowisku rozmieszczono 18 stacji bazowych oraz 3 regularne siatki punktów odbiorczych (użytkowników) zlokalizowane wzdłuż ulic. Łącznie w całym scenariuszu zdefiniowano $1\,184\,923$ punkty pomiarowe rozmieszczone w odstępach co $20\text{ cm}$. Rozmieszczenie stacji bazowych oraz siatek użytkowników przedstawiono na rysunkach 1 i 2.

Tak przygotowany model sceny stanowi wejście do symulatora Remcom Wireless InSite. W trakcie symulacji, na podstawie przyjętych parametrów konfiguracyjnych, wyznaczane są trajektorie promieni (ang. *ray tracing*), co pozwala określić parametry kanału radiowego dla każdej pary stacja bazowa–użytkownik. W scenariuszu `o1_60` (środowisko zewnętrzne, ang. *outdoor*, pasmo $60\text{ GHz}$) zastosowano następującą konfigurację:

- **Silnik symulacyjny i model propagacyjny:** komercyjny pakiet *Remcom Wireless InSite* (wersja 3.3) z modelem śledzenia promieni **X3D Ray Model** (wykorzystującym pełną akcelerację wielowątkową i GPU do wyznaczania trajektorii promieni w przestrzeni trójwymiarowej).
- **Częstotliwość nośna:** $f_c = 60\text{ GHz}$ (długość fali $\lambda = 5\text{ mm}$), odpowiadająca pasmu fal milimetrowych (pasmo V, ang. *V-band*).
- **Próg czułości detekcji promieni (ang. *power threshold*):** $-250\text{ dBm}$, co gwarantuje rejestrację nawet bardzo słabych składowych wielodrogowości przed ich odcięciem.
- **Mechanika emisji promieni (ang. *ray casting*):**
  - **Metoda:** równomierne sferyczne omiatanie przestrzeni (ang. *uniform sweep*).
  - **Rozdzielczość kątowa emisji (ang. *ray spacing*):** $0{,}25^\circ$ w obu płaszczyznach (azymutalnej i elewacyjnej).
  - **Zakres kątowy:** pełna sfera – azymut $360^\circ$ oraz elewacja $180^\circ$.
  - **Liczba wyemitowanych promieni:** dokładnie $259\,200$ promieni dla każdej pozycji stacji bazowej.
- **Interakcje fal elektromagnetycznych ze środowiskiem:**
  - **Maksymalna liczba odbić lustrzanych (ang. *max reflections*):** 4 odbicia (od ścian budynków oraz podłoża).
  - **Dyfrakcje na krawędziach (ang. *wedge diffractions*):** 0 (w paśmie 60 GHz zjawisko dyfrakcji na krawędziach budynków wnosi znikomy wkład energetyczny ze względu na wysokie tłumienie dyfrakcyjne, dlatego zostało wyłączone).
  - **Transmisja przez przeszkody (ang. *transmissions*):** 0 (ściany budynków traktowane są jako nieprzenikliwe dla fal milimetrowych, co odzwierciedla rzeczywiste tłumienie penetracji zewnętrznych przegród budowlanych przekraczające 40–60 dB).
  - **Odbicia od podłoża (ang. *terrain reflections*):** uwzględnione.
  - **Rozpraszanie dyfuzyjne (ang. *diffuse scattering*):** wyłączone.
- **Właściwości materiałowe obiektów 3D:**
  - **Budynki (32 obiekty):** zamodelowane z wykorzystaniem materiału bibliotecznego `ITU Layered drywall 3.5 GHz` (płyta gipsowo-kartonowa wg zalecenia ITU-R P.2040: przenikalność względna $\varepsilon_r = 2{,}94$, przewodność $\sigma = 0{,}02815\text{ S/m}$, grubość $13\text{ mm}$); przy wyłączonej transmisji skrośnej parametry te wpływają na współczynnik odbicia promieni od elewacji.
  - **Nawierzchnia drogowa i teren (*newTerrain*):** model wilgotnej ziemi/asfaltu (ang. *Wet earth*: $\varepsilon_r = 25{,}0$, $\sigma = 0{,}02\text{ S/m}$).
- **Anteny referencyjne w fazie ray-tracingu:** anteny izotropowe (o zysku $0\text{ dBi}$) o polaryzacji pionowej, co umożliwia późniejszą elastyczną syntezę dowolnych macierzy antenowych Massive MIMO w narzędziu DeepMIMO.
- **Rejestrowane parametry wyjściowe dla każdej ścieżki wielodrogowości:**
  - Kąt nadejścia fali do odbiornika (AoA, ang. *Angle of Arrival*) w azymucie i elewacji,
  - Kąt odejścia fali z nadajnika (AoD, ang. *Angle of Departure*) w azymucie i elewacji,
  - Opóźnienie czasowe propagacji (ToA, ang. *Time of Arrival*),
  - Zespolona odpowiedź impulsowa kanału (CIR, ang. *Complex Impulse Response*) oraz tłumienie ścieżki (ang. *pathloss*).

To właśnie wynik ray-tracingu jest przedmiotem analizy w niniejszej pracy. Przykładową symulację propagacji wielodrogowej w przestrzeni trójwymiarowej przedstawiono na rysunku 3.

![Rysunek 1. Widok z góry (ang. *top view*) scenariusza O1_60 z rozmieszczeniem stacji bazowych (BS) oraz siatek użytkowników (źródło: DeepMIMO [@deepmimo_website]).](../outputs/figures/the%20top%20view%20o1_60.png)

![Rysunek 2. Widok z lotu ptaka (ang. *bird-eye view*) modelu trójwymiarowego kanionu miejskiego w scenariuszu O1_60 (źródło: DeepMIMO [@deepmimo_website]).](../outputs/figures/the%20bird-eye%20view%20o1_60.png)

![Rysunek 3. Wizualizacja przestrzenna mechanizmu ray-tracingu w trójwymiarowym kanionie miejskim (scenariusz O1_60): (A) perspektywa 3D z góry przedstawiająca geometrię budynków, maszty stacji bazowych (z=6 m) i trajektorie promieni wielodrogowości wraz z rzutowaniem punktów odbić; (B) widok 3D wzdłuż kanionu z niskiej perspektywy eksponujący pionowe rozdzielenie ścieżki bezpośredniej LOS (w powietrzu) od odbicia od nawierzchni jezdni oraz odbić elewacyjnych od ścian budynków.](../outputs/figures/ray_tracing_wizualizacja.png)

## 2.2. Opis cech i zmiennych

### 2.2.1. Przygotowanie danych wejściowych i wyjściowych dla uczenia maszynowego

Stacje bazowe umieszczone są na wysokości 6 metrów nad poziomem terenu. Konfiguracja macierzy antenowej stacji bazowej w łączu w dół (ang. *downlink*) charakteryzuje się następującymi parametrami:

- **Układ tablicy:** płaski panel $Y\text{--}Z$ o rozmiarze $32 \times 8$:
  - **Łączna liczba anten:** $32 \times 8 = \mathbf{256}$ elementów antenowych na każdą stację bazową.
- **Odstęp między elementami antenowymi:** $0{,}5\lambda$ (odstęp półfalowy, $2{,}5\text{ mm}$ przy częstotliwości $60\text{ GHz}$).
- **Typ elementu:** dipol półfalowy (ang. *halfwave-dipole*).

W łączu w górę (ang. *uplink*) stacja bazowa odbiera sygnał pilotowy za pomocą pojedynczego pionowego dipola półfalowego, charakteryzującego się dookólną charakterystyką promieniowania w płaszczyźnie azymutu (ang. *omnidirectional*).

Terminal użytkownika (ang. *User Equipment*, UE) wyposażono w pojedynczy dipol półfalowy umieszczony na wysokości $2\text{ m}$ nad poziomem terenu. Układ nadawczo-odbiorczy tworzy zatem konfigurację MISO (ang. *Multiple-Input Single-Output*).

Dane wejściowe i wyjściowe do uczenia maszynowego przygotowano przy pomocy biblioteki DeepMIMO na podstawie scenariusza ray-tracingowego `o1_60`. Szczegółowe zestawienie parametrów konfiguracyjnych podano w tabeli 1. 

Tabela 1. Zestawienie parametrów konfiguracyjnych generatora kanałów DeepMIMO.

| Grupa parametrów | Parametr | Wartość w symulacji | Jednostka / Typ | Opis merytoryczny i uzasadnienie |
| :--- | :--- | :--- | :--- | :--- |
| **Scenariusz i stacje bazowe** | Scenariusz ray-tracingowy | `o1_60` | tekstowy | Model kanionu miejskiego (*outdoor*, 60 GHz) Remcom Wireless InSite. |
| | Aktywne stacje bazowe (`active_BS`) | BS 3, BS 4, BS 5, BS 6 | lista identyfikatorów | 4 skoordynowane stacje bazowe otaczające analizowany odcinek ulicy (w DeepMIMO v4: `tx_set_id = [4, 7, 3, 6]`). |
| | Liczba ścieżek wielodrogowości (`num_paths`) | 5 | całkowity | 5 najsilniejszych składowych propagacji wielodrogowej (w paśmie 60 GHz energia skupiona jest w składowej LOS i 4 pierwszych odbiciach). |
| **Siatka użytkowników (UE)** | Aktywny zbiór odbiorników (`rx_sets`) | Siatka `RX_1` (id: 0) | indeks zbioru | Główna siatka użytkowników biegnąca wzdłuż kanionu miejskiego. |
| | Zakres wierszy użytkowników | Od wiersza 1000 do 1300 | 1-based (w DeepMIMO v4: `0..300` w ramach wycinka) | 301 kolejnych wierszy wzdłuż osi $Y$ ($y \in [497\text{ m}, 557\text{ m}]$). |
| | Łączna liczba pozycji użytkowników | $301 \times 181 = \mathbf{54\,481}$ | całkowity | Liczba punktów odbiorczych (181 kolumn $\times$ 301 wierszy przy siatce o kroku 20 cm). |
| **Macierz antenowa BS** | Rozmiar i orientacja macierzy (`bs_antenna.shape`) | $32 \times 8$ (panel $Y\text{--}Z$) | $M_y \times M_z$ | Płaska macierz UPA: 32 kolumny w poziomie (azymut) $\times$ 8 wierszy w pionie (elewacja), łącznie **256 elementów**. |
| | Odstęp międzyszykowy (`spacing`) | $0{,}5$ | $\lambda$ ($2{,}5\text{ mm}$) | Standardowy odstęp półfalowy minimalizujący listki boczne (ang. *grating lobes*). |
| | Charakterystyka promieniowania elementu | `halfwave-dipole` | kategoryczny | Pionowy dipol półfalowy o zysku $2{,}15\text{ dBi}$. |
| **Antena terminala UE** | Rozmiar macierzy UE (`ue_antenna.shape`) | $1 \times 1$ | $M_y \times M_z$ | Pojedyncza antena odbiorcza (konfiguracja MISO). |
| | Charakterystyka promieniowania | `halfwave-dipole` | kategoryczny | Pojedynczy dipol półfalowy o dookólnej charakterystyce w azymucie. |
| **Modulacja wielotonowa OFDM** | Szerokość pasma systemu (`bandwidth`) | $500\text{ MHz}$ ($0{,}5\text{ GHz}$) | MHz / GHz | Szerokopasmowy kanał transmisyjny w paśmie fal milimetrowych (V-band). |
| | Całkowita liczba podnośnych (`subcarriers`) | 1024 | całkowity | Odstęp między podnośnymi: $\Delta f = \frac{500\text{ MHz}}{1024} \approx 488{,}28\text{ kHz}$. |
| | Wybrane podnośne pilotowe (`selected_subcarriers`) | Pierwsze 64 podnośne | wektor indeksów (`0..63`) | Rzeczywisty wycinek pasma estymacji pilotowej ($64 \times \Delta f = 31{,}25\text{ MHz}$). |
| | Krok próbkowania podnośnych (`subcarriers_sampling`) | 1 | całkowity | Brak podpróbkowania – wykorzystanie wszystkich pierwszych 64 podnośnych. |
| | Domena częstotliwości (`freq_domain`) | `True` | logiczny | Generowanie zespolonych transmitancji kanałowych $H[k]$ dla każdej podnośnej OFDM. |
| | Filtr dolnoprzepustowy odbiornika (`rx_filter`) | `False` | logiczny | Wyłączenie filtru kształtującego pasmo w celu zachowania surowej odpowiedzi kanału. |
| | Zjawisko Dopplera (`doppler`) | `False` | logiczny | Pominięcie dynamicznego przesunięcia Dopplera (statyczne migawki kanału w punktach siatki). |
| **Książka kodowa i model szumu** | Książka kodowa kształtowania wiązki (Codebook) | Macierz DFT $256 \times 512$ | zespolona macierz | Dwukrotne nadpróbkowanie w płaszczyźnie azymutu (`oversampling_rate = [1, 2, 1]`), dające $64 \times 8 = \mathbf{512}$ kierunków wiązek na stację bazową. |
| | Współczynnik szumów odbiornika (NF) | $5\text{ dB}$ | dB | Typowa wartość szumów własnych głowicy odbiorczej RF stacji bazowej w paśmie 60 GHz. |
| | Zysk przetwarzania estymacji (Processing Gain) | $10\text{ dB}$ | dB | Zysk z koherentnej korelacji sekwencji pilotującej podczas estymacji kanału w łączu w górę. |
| | Gęstość widmowa mocy szumu | $-204\text{ dBW/Hz}$ | dBW/Hz | Odpowiada $-174\text{ dBm/Hz}$ (szum termiczny w temperaturze pokojowej $T_0 = 290\text{ K}$). |

### 2.2.2. Zestawienie cech i zmiennych w zbiorze danych

Zbiór zawiera [N] obserwacji oraz [M] cech (zmiennych objaśniających) oraz zmienną celu `[nazwa_targetu]`.

Tabela 2. Zestawienie cech w zbiorze danych.

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

Do zidentyfikowanych ograniczeń analizowanego zbioru danych należą:
- **Uproszczenie właściwości materiałowych fasad budynków:** W scenariuszu `o1_60` bryły budynków zamodelowano przy użyciu materiału bibliotecznego `ITU Layered drywall 3.5 GHz` o stałych elektrycznych właściwych dla płyty gipsowo-kartonowej w paśmie 3,5 GHz ($\varepsilon_r = 2{,}94$, $\sigma = 0{,}02815\text{ S/m}$), co stanowi uproszczenie względem rzeczywistych materiałów elewacyjnych (beton, szkło) w paśmie 60 GHz. Ze względu na zdefiniowany w symulacji brak transmisji skrośnej (`max_transmissions = 0`), parametry te wpływają wyłącznie na wartości współczynnika odbicia Fresnela od powierzchni budynków.
- [Dalsze ograniczenia zbioru danych: syntetyczny i deterministyczny charakter ray-tracingu, brak dynamicznych przeszkód i obiektów ruchomych, wyłączenie dyfrakcji i rozpraszania dyfuzyjnego...]

\newpage
