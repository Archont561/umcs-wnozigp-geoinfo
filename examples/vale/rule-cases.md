# Fixture: expected PLTechnical findings

This file is a test fixture for the local Vale preset. Every section states the finding
it is meant to produce, so a change in the rules shows up as a change here.

Expectations below were corrected against the rule definitions after a first run
disagreed with the draft assumptions. See SPEC-EDIT for the measurement record.

## Bureaucratic phrasing — expected: 1 suggestion, on the heading only

## W dniu dzisiejszym wykonano pomiar

W dniu dzisiejszym wykonano pomiar.

## Pleonasms — expected: 1 suggestion, on the heading only

## W okresie czasu zebrano dane

W okresie czasu zebrano dane.

## Verb phrases — expected: 4 suggestions — the heading, the heading phrase in prose, and both passive forms

## Dokonano analizy wyników

Dokonano analizy wyników.

Została przeprowadzona analiza ryzyka.

Zostały przeprowadzone analizy.

## Unit spacing — expected: 4 warnings (20cm, 5kg, 20°C, 20cm again)

Próbka ma długość 20cm.

Masa wynosiła 5kg.

Poprawny zapis to 20 cm i 5 kg.

Temperatura wynosiła 20°C — the degree symbol is **not** an exception, contrary to the heading.

Kod `20cm` w kodzie jest pomijany.

Adres `https://example.org/20cm/nie-zmieniaj` nie jest sprawdzany.

## Long sentences — expected: 1 suggestion above 30 tokens

Ten przykład zdania został celowo rozbudowany o wiele kolejnych określeń, aby przekroczyć próg trzydziestu tokenów przyjęty w tym profilu redakcyjnym i pokazać, że długość zdania jest wyłącznie wskazówką dla redaktora, a nie normą poprawności językowej ani akademickiej.

Krótkie zdanie jest poprawne.

## Clean control — expected: 0 findings

Pomiar wykonano 12 maja. Wynik zapisano w tabeli 3.

Przeprowadzono analizę ryzyka, a wynik zapisano w tabeli 4.

Próbkę opisano w rozdziale drugim.
