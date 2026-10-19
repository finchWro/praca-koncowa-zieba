# 1. Wstęp

<!-- Wymagania formalne: 2–3 strony.
Elementy obowiązkowe:
- Kontekst biznesowy / naukowy oraz uzasadnienie wyboru tematu.
- Jasno sformułowany cel główny pracy.
- Od 1 do 3 konkretnych, weryfikowalnych pytań badawczych.
- Krótki przegląd literatury i dotychczasowych rozwiązań dziedzinowych.
-->

## 1.1. Kontekst i uzasadnienie tematu 

Operatorzy telekomunikacyjni (ang. Communication Service Providers, CSP) działają na silnie konkurencyjnym rynku, który wymaga ciągłej redukcji kosztów. Największe nakłady inwestycyjne związane są z zakupem pasma na licytacjach krajowych. Efektywne wykorzystanie tego zasobu decyduje o przewadze konkurencyjnej na rynku usług telekomunikacyjnych. Miarą efektywności użycia pasma jest efektywność spektralna (ang. spectral efficiency), która definiowana jest jako przepływność binarna (liczba przesłanych bitów na sekundę) przypadająca na jednostkę szerokości pasma [bit/s/Hz].

W celu poprawy efektywności spektralnej operatorzy wykorzystują w sieciach komórkowych technologię Massive MIMO (ang. Multiple Input Multiple Output), która wykorzystuje macierze antenowe o liczbie elementów znacznie przekraczającej liczbę jednocześnie obsługiwanych użytkowników. Dzięki zwielokrotnieniu przestrzennemu (ang. spatial multiplexing) możliwa jest jednoczesna transmisja do wielu użytkowników w tym samym zasobie częstotliwościowym i czasowym, co bezpośrednio zwiększa efektywność spektralną systemu [@sharetechnote_massive_mimo].

Aby dalej poprawić efektywność spektralną, organizacja standaryzująca 3GPP przeprowadziła analizę możliwości wykorzystania uczenia maszynowego w telekomunikacji. W efekcie powstał raport techniczny TR 38.843 "Study on Artificial Intelligence (AI)/Machine Learning (ML) for NR air interface", w którym opisano scenariusz predykcji wiązki w dziedzinie przestrzennej (ang. spatial domain beam prediction), polegający na wyznaczeniu optymalnego wektora kształtowania wiązki na podstawie sygnałów pilotażowych o zredukowanej liczbie pomiarów.

W pracy [@alkhateeb2018deep] zaproponowano architekturę skoordynowanego kształtowania wiązki z wykorzystaniem głębokich sieci neuronowych dla systemów fal milimetrowych, która pozwala na znaczne ograniczenie narzutu pilotowego. Niniejsza praca nawiązuje do tej metodyki, stanowiąc jej replikację i próbę optymalizacji w wybranym scenariuszu.

W pracy wykorzystano zbiór danych wygenerowany za pomocą frameworku DeepMIMO (Arizona State University), opartego na danych z symulacji ray-tracingowych przeprowadzonych w oprogramowaniu Remcom Wireless InSite dla scenariusza 3GPP 5G NR outdoor [@Alkhateeb2019].

## 1.2. Cel pracy i pytania badawcze

Głównym celem niniejszej pracy jest implementacja scenariusza predykcji wiązki w dziedzinie przestrzennej (zdefiniowanego w raporcie technicznym 3GPP TR 38.843) z wykorzystaniem modeli uczenia maszynowego w języku Python. Praca obejmuje analizę osiągniętej efektywności spektralnej oraz jej porównanie z metodami konwencjonalnymi, opartymi na wyczerpującym przeszukiwaniu wiązek i pomiarach pilotowych [@3gpp_tr38843].

W ramach pracy postawiono następujące pytania badawcze:
1. **PB1:**  Czy modyfikacja architektury modelu lub wstępnego przetwarzania cech pozwala uzyskać wyższą efektywność spektralną w porównaniu z rozwiązaniem bazowym przedstawionym przez Alkhateeba i in. [@alkhateeb2018deep]?

## 1.3. Przegląd literatury 

Organizacja standaryzująca 3rd Generation Partnership Project (3GPP) wraz z pierwszym wydaniem 5G-Advanced rozpoczęła prace nad wykorzystaniem AI/ML w sieciach telekomunikacyjnych [@lin2023overview]. W ramach grupy TSG RAN (głównie RAN1) opracowano raport techniczny TR 38.843, opisujący wyniki studium nad zastosowaniem AI/ML w interfejsie radiowym NR [@3gpp_tr38843]. W dokumencie wytypowano trzy przypadki użycia, dla których przeprowadzono badania i które stanowią punkt odniesienia dla prac w tym obszarze:

1. CSI Feedback

2. Beam Management 

3. Positioning 

Aby umożliwić prowadzenie badań i reprodukcję wyników, powstały środowiska, które pozwalają generować zbiory danych dla różnych scenariuszy (np. DeepMIMO [@Alkhateeb2019] czy Sionna [@hoydis2022sionna]).

Alkhateeb i in. badali scenariusz predykcji wiązki wykorzystaniem danych z symulacji ray-tracingowych, które stały się podstawą zbioru DeepMIMO [@Alkhateeb2019]. Wyniki badań wykazały, że ich model głebokiej sieci neuronowej pozwala na poprawienie efektywności spektralnej w prówaniu do metod klasycznych (wykonywania pomiarów na wszystkich wiązkach pilotowych i selekcji najlepszej).



\newpage
