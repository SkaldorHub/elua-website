# Inhalte, Platzhalter und Rechtliches

## Inhaltsregeln

Die Aussagen der Seite stammen von der Referenzseite https://www.familienmusizieren.com/chor-elua/ und dürfen inhaltlich nicht verändert werden, auch nicht die Schreibweisen ("a capella", "Herren-Chor", "Herrenensembles"). Nur Layout und Darstellung sind frei.

Reihenfolge der Startseite:

1. Titel "Elua" und Untertitel "ein junger A Cappella Herren-Chor"
2. Chorfoto
3. Intro-Satz
4. Banner "Neue Chorsänger sind willkommen!"
5. Kontakt
6. Entstehung des Chores
7. Leitung
8. Auftritte
9. Auswahl aus den Programmen (Popsongs, Klassische Männerchöre aus allen Epochen)
10. Footer mit Link zum Impressum

Bewusst nicht übernommen: "Wir unterstützen" und die Förderer-Logos der Referenzseite (sie gehören zum Trägerverein) sowie die Buttons "Konzerte" und "Buchen Sie uns" (auf Wunsch entfernt).

## Herkunft der Kontakt- und Impressumsdaten

Elua ist ein Ensemble des Vereins **Familienmusizieren e.V.**. Anbieter der Seite ist deshalb der Verein.

- **Impressum** (`/impressum/`): Angaben aus dem Impressum des Vereins (https://www.familienmusizieren.com/about/): Vereinsname, Anschrift, Vereinsregister VR 33933 B (Amtsgericht Berlin-Charlottenburg), vertreten durch und redaktionell verantwortlich Rosemarie Arzt, Telefon und E-Mail des Vereins. Angepasst wurde nur die Rechtsgrundlage: "§ 5 DDG" statt des veralteten "§ 5 TMG". Der Absatz zur Verbraucherstreitbeilegung stammt aus dem e-recht24-Generator, dessen Quellenangabe deshalb stehen bleibt.
- **Startseite, Abschnitt Kontakt:** Mail `info@elua-chor.de` wie auf der Referenzseite.
- Ändern sich die Vereinsdaten (Adresse, Vorstand, Registernummer), das Impressum im Cloud-Editor anpassen und Deploy auslösen. Die Daten müssen mit dem Impressum des Vereins übereinstimmen.
- Ein Bildnachweis fehlt bewusst. Falls der Fotograf genannt werden soll, im Impressum ergänzen.

## Warum ein Impressum nötig ist

Kein Rechtsrat. Für eine verbindliche Auskunft den Verein oder eine Rechtsberatung fragen.

- In Deutschland müssen Anbieter digitaler Dienste, die "geschäftsmäßig" betrieben werden, ein Impressum bereithalten (§ 5 Digitale-Dienste-Gesetz, DDG). Geschäftsmäßig heißt: auf Dauer angelegt und mit wirtschaftlichem Bezug. Gewinnabsicht ist dafür nicht nötig, ein Verein ist nicht ausgenommen.
- Ausgenommen sind rein private Seiten ohne wirtschaftlichen Bezug (etwa Familienfotos). Die Chor-Seite ist öffentlich, wirbt um neue Sänger und beschreibt Auftritte bei Events, Festivals und Konzertreihen. Das ist ein Außenauftritt mit wirtschaftlichem Bezug. Ein Impressum ist deshalb praktisch Pflicht. Gemeinnützigkeit ändert daran nichts, und das Entfernen des Buchungsangebots reicht nicht aus.
- Bei redaktionellen Inhalten kommt § 18 Abs. 2 Medienstaatsvertrag dazu: eine verantwortliche Person mit Name und Anschrift.
- Ein fehlendes oder fehlerhaftes Impressum kann kostenpflichtig abgemahnt werden, und es sind Bußgelder möglich.
- Inhalt: Name und Anschrift des Vereins, Vertretungsberechtigte (beim Verein der Vorstand), schnelle elektronische Kontaktmöglichkeit (E-Mail) plus ein zweiter Kontaktweg, Registereintrag bei eingetragenem Verein, verantwortliche Person nach § 18 MStV.
- Es muss leicht erkennbar und direkt erreichbar sein. Deshalb steht der Link im Footer jeder Seite.

## Datenschutzerklärung

Zusätzlich zum Impressum ist eine Datenschutzerklärung nötig (DSGVO). GitHub Pages verarbeitet beim Aufruf IP-Adressen in Server-Logs, das muss benannt werden. Die Seite selbst nutzt keine Cookies, kein Tracking und keine externen Schriften. Eine Vorlage dafür ist noch nicht angelegt.

## Bildrechte

Das Chorfoto ist laut Team eigenes Material. Den Urheber im Impressum unter "Bildnachweis" nennen.

## Design und Tokens

Das Design ist in Webstudio über **Design-Tokens** aufgebaut (etwa 50 Stück): Farben, Schriftgrößen, Abstände, Karten, Navigation, Footer. Ein Element trägt mehrere Tokens, lokale Styles gibt es nur noch für wenige Einzelfälle. Für Tablet, Mobile landscape und Mobile portrait sind an den Tokens eigene Werte hinterlegt (kleinere Abstände und Schriften, die Farbverlauf-Kreise im Kopf entfallen auf dem Handy).

Eckdaten für ein einheitliches Erscheinungsbild: hell und modern, Systemschrift, große fette Überschriften, Tinte `#14122b`, Akzent Indigo `#4f46e5`, Flächen `#f4f3fa`, Linien `#e7e6f0`, gedämpfter Text `#5b5a70`.

**Wo man was ändert:**

- **Im Builder** (Style-Panel, Tokens): Eine Farbe oder Größe an einem Token ändern wirkt auf alle Elemente, die es nutzen. Das ist der bequeme Weg für Feinschliff.
- **Im Repo** (`design/tokens.json` plus `scripts/apply-design.py`): Für Umbauten in größerem Stil, siehe [selfhost-editing.md](selfhost-editing.md).
- **Nur eine Quelle pflegen.** Änderungen im Builder landen nicht in `design/tokens.json`. Wer danach das Skript ausführt, überschreibt sie. Entweder ihr pflegt das Design im Builder (dann ist `design/` nur der Ausgangsstand), oder im Repo (dann werden Builder-Änderungen vor dem Einspielen dort nachgetragen).

Nicht umgesetzt: wiederverwendbare Komponenten. Navigation und Footer sind pro Seite eigene Elemente, weil sie sich unterscheiden (Anker auf der Startseite, Rücklink im Impressum). Bei mehr Seiten wäre ein geteilter Kopf- und Fußbereich (Webstudio "Slot") sinnvoll.

## Offene Punkte

- Das Design des Abschnitts "Auswahl aus den Programmen" (zwei Karten mit Listen) ist noch nicht abgenommen.
- Datenschutzerklärung (Vorlage fehlt noch, der Verein hat auf familienmusizieren.com eine unter `/j/privacy`).
- Eigene Domain (siehe [dns-domain.md](dns-domain.md)).
