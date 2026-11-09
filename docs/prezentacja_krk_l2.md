---
marp: true
theme: default
size: 16:9
paginate: true
header: "KRK L2 AI/ML Discussion Forum | Błażej Zięba"
footer: "Maksymalizacja efektywności spektralnej w sieciach 5G/6G Massive MIMO przy pomocy predykcji wiązki w dziedzinie przestrzeni"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  footer {
    font-size: 0.55rem;
    color: #555;
  }
  header {
    font-size: 0.55rem;
    color: #555;
  }
  .highlight {
    background-color: #f7f9fa;
    border-left: 4px solid #107c41;
    padding: 10px 15px;
    border-radius: 4px;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.2rem;
  }
  code {
    background-color: #eee;
    padding: 2px 5px;
    border-radius: 3px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Deep Learning-based Spatial Beamforming
### From Ray-Tracing and DeepMIMO to Real-Time Inference in 5G-Advanced

**Prezenter:** Błażej Zięba  
**Forum:** KRK L2 AI/ML Discussion Forum  
**Kontekst:** 3GPP Rel-18 (TR 38.843) / 5G mmWave Beam Management  
**Data:** Listopad 2026

<!-- note:
-->

---

# Agenda spotkania

1. **AI assisted work. Konfiguracja środowiska pracy**  
2. **Wybór tematu**  
3. **Luka badawcza**  
4. **Biblioteka DeepMIMO**  
5. **Model systemu**  
6. **Raport z postępu prac**  

<!-- note:
-->

---

# AI assisted work. Konfiguracja środowiska pracy

- **Środowisko analityczno-badawcze (Python / Deep Learning):**
  - Linux, Python 3.10+, PyTorch, NumPy, SciPy, Scikit-learn.
  - Pakiet **DeepMIMO v4** do syntezy kanałów radiowych z symulacji ray-tracingowych.

- **Paradygmat „Everything as Code” i wersjonowanie (Git):**
  - **Praca i dokumentacja:** Czysty Markdown (`praca/chapters/*.md`) z automatyczną kompilacją Pandoc do `.docx` / `.pdf`.
  - **Prezentacje:** Format **Marp Markdown** – prezentacje jako kod, pełna wersjonowalność diffów i natywny podgląd.

- **Agentowe wsparcie AI w procesie badawczym (Antigravity / LLM Pair-Programming):**
  - Zestaw dedykowanych reguł projektowych (`AGENTS.md`): polska nomenklatura i standardy PWr.
  - Dedykowane skille AI: automatyczny recenzent tekstu merytorycznego, menedżer bibliografii (`references.bib`) oraz weryfikator formalny kryteriów oceny.

<div class="highlight" style="margin-top: 20px; font-size: 0.9rem;">
<strong>Kluczowa korzyść:</strong> Całość repozytorium (kod, dane konfiguracyjne, praca pisemna i slajdy) opiera się na formatach tekstowych, co umożliwia ciągłą analizę, walidację i współpracę z agentami AI w jednym zintegrowanym środowisku.
</div>

<!-- note:
W pierwszym punkcie chciałbym krótko przedstawić metodykę pracy i warsztat narzędziowy.
Cały projekt został zorganizowany według filozofii "Everything as Code". Zarówno kod modeli w PyTorch, jak i tekst samej pracy w Markdownie oraz slajdy w formacie Marp to czyste pliki tekstowe pod kontrolą Gita.
Dzięki temu mogłem w pełni wykorzystać asystenta AI nie tylko do pomocy przy kodzie czy debugowaniu, ale również do weryfikacji metodologicznej - np. pilnowania braku data leakage, zarządzania cytowaniami w BibTeX czy tworzenia slajdów.
-->
