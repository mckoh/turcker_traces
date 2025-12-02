# 🚛 Fahrzeugdatenauswertung (`trucker_traces`)

Die Fahrerkartendaten entstehen direkt im LKW: Der Fahrer steckt zu Beginn seiner Tätigkeit die Fahrerkarte ein und wählt jeweils manuell aus, ob er gerade fährt, arbeitet (z. B. Be- oder Entladen) oder eine Pause/Ruhezeit nimmt. Diese Informationen werden kontinuierlich auf der Karte gespeichert. Anschließend können die Fahrerkartendaten als Excel-Dateien heruntergeladen werden und enthalten eine chronologische Auflistung der Tätigkeiten der Fahrer: Lenkzeit, Arbeitszeit und Ruhezeit. Diese Tätigkeiten bilden gemeinsam die Einsatzzeit, die wiederum der Schichtzeit bzw. einer Tour eines Fahrers entspricht.

## 🎯 Problemstellung

Das zentrale Problem besteht darin, dass aus den Rohdaten nicht automatisch erkennbar ist, wann eine Schicht beginnt und wann sie endet. Technisch beginnt die Schicht mit dem Einstecken der Fahrerkarte und endet mit dem Herausziehen, da anschließend automatisch Ruhezeit gebucht wird. Diese Logik ist jedoch in den Excel-Auszügen nicht direkt ablesbar, sodass Schichten nicht automatisch voneinander getrennt werden können. Bei größeren Datenmengen führt dies zu einem großen manuellen Aufwand.

Zusätzlich sollen **Pausen** innerhalb einer Schicht analysiert werden, insbesondere Pausen **über 30 Minuten**, **über 1 Stunde** und **über 2 Stunden**. Ruhezeiten treten jedoch sowohl am tatsächlichen Schichtende als auch als Pausen während der Schicht auf. Excel kann diese beiden Fälle nicht voneinander unterscheiden, und zusammenhängende Ruhezeiten, die sich über zwei Kalendertage erstrecken, werden ebenfalls nicht als Einheit erkannt. Ein Beispiel ist ein Fahrer, der spät am Abend beginnt und über Mitternacht hinweg eine Pause macht – diese wird im Export als zwei getrennte Ruhezeitblöcke angezeigt, obwohl es sich um eine einzige Pause handelt.

## 🪜 Vorgehen

Um die Fahrerkartendaten sinnvoll auswerten zu können, wäre es daher notwendig **folgende Dinge zu ermitteln**:

* Schichtanfang und -ende zu erkennen,
* die Gesamtdauer einer Schicht zu berechnen,
* die einzelnen Tätigkeiten (Lenkzeit, Arbeitszeit, Ruhezeit) pro Schicht zu summieren,
* Pausen innerhalb der Schicht (>30 Min, >1 h, >2 h) zuverlässig zu identifizieren.