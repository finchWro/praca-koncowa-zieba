# 1. Wstęp

<!-- Wymagania formalne: 2–3 strony.
Elementy obowiązkowe:
- Kontekst biznesowy / naukowy oraz uzasadnienie wyboru tematu.
- Jasno sformułowany cel główny pracy.
- Od 1 do 3 konkretnych, weryfikowalnych pytań badawczych.
- Krótki przegląd literatury i dotychczasowych rozwiązań dziedzinowych.
-->

## 1.1. Kontekst i uzasadnienie tematu 

Operatorzy telekomunikacyjni (ang. Communication Service Providers, CSP) działają na silnie konkurencyjnym rynku, który wymaga ciągłej redukcji kosztów. Jednym z największych kosztów operatorów jest pozyskanie pasma w aukcjach krajowych [@gsma2018spectrum_pricing]. Efektywne wykorzystanie tego zasobu decyduje o przewadze konkurencyjnej na rynku usług telekomunikacyjnych. Miarą efektywności użycia pasma jest efektywność spektralna (ang. spectral efficiency), która definiowana jest jako przepływność binarna (liczba przesłanych bitów na sekundę) przypadająca na jednostkę szerokości pasma [bit/s/Hz].

W celu poprawy efektywności spektralnej operatorzy stosują w sieciach komórkowych technologię Massive MIMO (ang. Multiple Input Multiple Output), która wykorzystuje macierze antenowe o liczbie elementów znacznie przekraczającej liczbę jednocześnie obsługiwanych użytkowników. Dzięki zwielokrotnieniu przestrzennemu (ang. spatial multiplexing) możliwa jest jednoczesna transmisja do wielu użytkowników w tym samym zasobie częstotliwościowym i czasowym, co bezpośrednio zwiększa efektywność spektralną systemu [@marzetta2010noncooperative; @bjornson2017massive].

Organizacja 3GPP (ang. 3rd Generation Partnership Project) w ramach prac nad standardem 5G-Advanced (Release 18) przeanalizowała zastosowanie uczenia maszynowego w interfejsie radiowym, m.in. do predykcji wiązki przy ograniczonej liczbie pomiarów, co pozwala zmniejszyć narzut sygnalizacyjny i podnieść efektywność spektralną [@3gpp_tr38843].

Alkhateeb i in. [@alkhateeb2018deep] zaproponowali architekturę skoordynowanego kształtowania wiązki z wykorzystaniem głębokich sieci neuronowych dla systemów fal milimetrowych, która pozwala na znaczne ograniczenie narzutu pilotowego. Niniejsza praca nawiązuje do tej metodyki, stanowiąc jej replikację i próbę optymalizacji w wybranym scenariuszu.

W niniejszej pracy wykorzystano zbiór danych DeepMIMO v4 [@deepmimo_website] (Arizona State University) dla scenariusza O1 (ulica w mieście, 60 GHz), opartego na symulacjach ray-tracingowych w programie Remcom Wireless InSite [@Alkhateeb2019].

## 1.2. Cel pracy i pytania badawcze

Głównym celem pracy jest implementacja i ocena modelu uczenia głębokiego do skoordynowanego kształtowania wiązki (ang. Deep Learning Coordinated Beamforming) w dziedzinie przestrzennej, zgodnie ze scenariuszem opisanym w raporcie 3GPP TR 38.843 [@3gpp_tr38843] oraz metodyką Alkhateeba i in. [@alkhateeb2018deep]. Na podstawie ograniczonej liczby dookólnych pomiarów pilotowych sieć neuronowa wyznacza wiązkę z predefiniowanej książki kodowej. Uzyskaną efektywność spektralną netto (ang. effective spectral efficiency) porównano z dwoma punktami odniesienia z pracy [@alkhateeb2018deep]: wyidealizowanym doborem wiązki bez narzutu treningowego (ang. Genie-Aided Coordinated Beamforming, górna granica wydajności) oraz konwencjonalną metodą bazową opartą na wyczerpującym przeszukiwaniu książki kodowej z uwzględnieniem narzutu czasowego na trening wiązek (ang. Baseline Coordinated Beamforming).

W ramach pracy postawiono następujące pytania badawcze:
1. **PB1:** Czy model wytrenowany na danych DeepMIMO v4 (scenariusz O1, 60 GHz) osiąga efektywność spektralną różniącą się o nie więcej niż 5% od wyników Alkhateeba i in. [@alkhateeb2018deep] przy tej samej liczbie anten i książce kodowej?
2. **PB2:** Jak zmiana architektury sieci (liczba warstw, liczba neuronów) i hiperparametrów treningu wpływa na efektywność spektralną oraz liczbę parametrów i czas inferencji modelu?
3. **PB3:** Czy możliwe jest uruchomienie modeli opracowanych w ramach PB1 i PB2 w środowisku NVIDIA AI Aerial bez zmian w architekturze i jakie są różnice w czasie inferencji oraz wymaganiach sprzętowych względem uruchomienia w PyTorch?

## 1.3. Przegląd literatury 

Organizacja standaryzująca 3GPP wraz z pierwszym wydaniem 5G-Advanced rozpoczęła prace nad wykorzystaniem AI/ML w sieciach telekomunikacyjnych [@lin2023overview]. W ramach grupy roboczej TSG RAN (ang. Technical Specification Group Radio Access Network) opracowano raport techniczny TR 38.843, opisujący wyniki studium nad zastosowaniem AI/ML w interfejsie radiowym NR (ang. New Radio) [@3gpp_tr38843]. W dokumencie wytypowano trzy przypadki użycia, dla których przeprowadzono badania i które stanowią punkt odniesienia dla prac w tym obszarze:

1. kompresja informacji zwrotnej o stanie kanału (ang. Channel State Information feedback, CSI feedback),
2. zarządzanie wiązką (ang. beam management), 
3. pozycjonowanie (ang. positioning).

W zarządzaniu wiązką wyróżniono predykcję w dziedzinie przestrzennej (BM-Case 1) i czasowej (BM-Case 2); niniejsza praca dotyczy pierwszego przypadku.

W konwencjonalnych systemach 5G NR procedury zarządzania wiązką opierają się na okresowym przemiataniu wiązek (ang. beam sweeping) przy użyciu bloków synchronizacji i kanału rozgłoszeniowego SS/PBCH (często określanych skrótowo jako bloki SSB, ang. Synchronization Signal and PBCH Block) oraz sygnałów referencyjnych CSI-RS (ang. Channel State Information Reference Signal) [@giordani2019tutorial]. Wraz ze wzrostem liczby elementów antenowych w pasmach fal milimetrowych wyczerpujące przeszukiwanie przestrzeni staje się źródłem znacznego narzutu czasowego i spadku przepływności, co motywuje poszukiwanie metod predykcyjnych opartych na AI/ML.

Alkhateeb i in. [@alkhateeb2018deep] zaproponowali uczenie głębokie do skoordynowanego kształtowania wiązki, wykorzystując dane z symulacji ray-tracingowych, na których oparto później zbiór DeepMIMO [@Alkhateeb2019]. Wykazali, że model osiąga przepływność bliską optymalnej przy znacznie mniejszym narzucie pilotowym.

Przegląd wyzwań związanych z zarządzaniem wiązkami z użyciem uczenia głębokiego przeprowadzili Ma i in. [@ma2023deep], zwracając szczególną uwagę na zagadnienia generalizacji modeli w zmiennych warunkach propagacyjnych oraz konieczność redukcji złożoności obliczeniowej sieci neuronowych (ang. Deep Neural Networks, DNN) poprzez kwantyzację i kompresję parametrów, co stanowi bezpośrednią motywację dla badań nad optymalizacją architektury w ramach pytania PB2.

Na potrzeby badań nad sztuczną inteligencją w warstwie fizycznej firma NVIDIA udostępniła otwartą bibliotekę Sionna, umożliwiającą akcelerowane na GPU symulacje łącza radiowego z różniczkowalnymi blokami przetwarzania sygnałów [@hoydis2022sionna]. Jej rozwinięciami są Sionna Research Kit, który pozwala uruchamiać modele w czasie rzeczywistym na stosie RAN [@cammerer2025sionna], oraz platforma NVIDIA AI Aerial, obejmująca m.in. akcelerowaną warstwę fizyczną i cyfrowego bliźniaka sieci [@cohenarazi2025aerial]. Możliwość przeniesienia modeli predykcji wiązki na platformę NVIDIA AI Aerial jest przedmiotem pytania badawczego PB3.

\newpage
