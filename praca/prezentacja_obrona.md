---
marp: true
theme: default
size: 16:9
paginate: true
header: "Maksymalizacja efektywności spektralnej w 5G/6G | Błażej Zięba"
footer: "Politechnika Wrocławska – Studia Podyplomowe Data Science"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  footer {
    font-size: 0.55rem;
    color: #666;
  }
  header {
    font-size: 0.55rem;
    color: #666;
  }
  .highlight {
    background-color: #f0f4f8;
    border-left: 4px solid #0056b3;
    padding: 10px 15px;
    border-radius: 4px;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Maksymalizacja efektywności spektralnej w sieciach 5G/6G Massive MIMO
### Predykcja wiązki w dziedzinie przestrzeni przy użyciu uczenia głębokiego

**Autor:** Błażej Zięba  
**Opiekun pracy:** dr inż. Natalia Piórkowska  
**Kierunek:** Studia Podyplomowe Data Science – Politechnika Wrocławska  
**Termin obrony:** 2027

<!-- note:
[Czas: 0:00 - 0:30]
Dzień dobry Państwu. Nazywam się Błażej Zięba. Tematem mojej pracy końcowej jest maksymalizacja efektywności spektralnej w sieciach 5G i 6G Massive MIMO przy pomocy predykcji wiązki w dziedzinie przestrzennej z wykorzystaniem modeli głębokiego uczenia.
-->

---

# Agenda wystąpienia (zgodnie z §8.1)

1. **Problem i cel pracy (ok. 1,5 min)**  
   *Wąskie pasmo, narzut procedur beam sweepingu w mmWave i cele badawcze (PB1–PB3).*
2. **Charakterystyka danych: Ray-tracing & DeepMIMO (ok. 2 min)**  
   *Symulacja elektromagnetyczna kanionu miejskiego i przygotowanie zbioru danych.*
3. **Metodyka i schemat procesu analitycznego (ok. 2,5 min)**  
   *Potok przetwarzania bez wycieku danych, model klasyfikacji i punkt odniesienia (Baseline).*
4. **Wyniki eksperymentów i ewaluacja (ok. 3 min)**  
   *Osiągnięta efektywność spektralna netto oraz kompromis złożoność–czas inferencji.*
5. **Wnioski, ograniczenia i wdrożenie (ok. 1 min)**  
   *Podsumowanie pytań badawczych i możliwości uruchomienia na platformie NVIDIA AI Aerial.*

<!-- note:
[Czas: 0:30 - 1:00]
Prezentację zaplanowałem na około 10 minut w układzie zgodnym z wymaganiami regulaminowymi. Skupię się na problemie biznesowo-technicznym, specyfice pozyskania danych z symulacji ray-tracingowej, schemacie procesu modelowania oraz uzyskanych wynikach efektywności spektralnej w odniesieniu do konwencjonalnego przeszukiwania wiązek.
-->

---

# Źródło danych: Od fizyki do systemu radiowego

<div class="columns">
<div>

### 1. Remcom Wireless InSite
*(Fizyka propagacji 3D)*
- **Środowisko:** kanion miejski 60 GHz (*outdoor*).
- **Zjawiska:** do 4 odbić od budynków i asfaltu.
- **Wynik fizyczny:**
  - Kąty nadejścia i odejścia (AoA / AoD),
  - Czas opóźnienia ścieżek ($\tau$ / ToA),
  - Zespolone tłumienie promieni.
- *Uniwersalny – niezależny od anten.*

</div>
<div>

### 2. Generator DeepMIMO v4
*(System telekomunikacyjny)*
- **Panel BS:** siatka $32 \times 8$ (**256 anten**).
- **Terminal:** pojedynczy dipol (MISO).
- **OFDM:** pasmo 500 MHz, 64 podnośne.
- **Transformacja:**
  - Nałożenie wektorów odpowiedzi szyku,
  - Sumowanie 5 najsilniejszych ścieżek,
  - **$X$:** wektor pilotowy uplink + szum (5 dB NF),
  - **$y$:** optymalna wiązka z książki (512 klas).

</div>
</div>

<div class="highlight" style="margin-top: 15px; font-size: 0.85rem;">
<strong>Kluczowy mechanizm:</strong> Dzięki fizycznej zasadzie wzajemności kanału (reciprocity), pojedynczy pilot dookólny nadany przez telefon pozwala sieci neuronowej odgadnąć optymalną wąską wiązkę stacji bazowej w łączu w dół.
</div>

<!-- note:
[Czas: 2:30 - 3:30]
Przejdźmy do danych. Dane nie pochodzą z prostego generatora losowego, lecz z dwuetapowej symulacji.
W pierwszym kroku profesjonalny raytracer Remcom Wireless InSite symuluje czystą fizykę odbić fal w trójwymiarowym kanionie miejskim dla pasma 60 GHz. Wyznacza on geometryczne parametry promieni: kąty, opóźnienia i tłumienia.
W drugim kroku biblioteka DeepMIMO nakłada na te promienie konkretną konfigurację systemu: 256-elementowy panel antenowy stacji bazowej oraz modulację OFDM.
W efekcie otrzymujemy wektor sygnałów pilotowych w łączu w górę jako wejście X oraz indeks najlepszej wiązki z 512 dostępnych kierunków jako etykietę Y.
-->
