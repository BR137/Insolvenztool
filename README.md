# Insolvenztool
- [German](#german) - german version
- [English](#english) - english version, more details

# German
Dieses Tool automatisiert Einzelanfragen an [insolvenzbekanntmachungen.de](https://neu.insolvenzbekanntmachungen.de/ap/) und [restrukturierungsbekanntmachung.de](https://www.restrukturierungsbekanntmachung.de/res-ap/). Das Ergebnis kann in ein logfile gespeichert werden und via Windows-Benachrichtigung ausgegeben werden. Das Tool kann manuell ausgeführt werden oder in den Windows Aufgabenplaner (Windows Task Schedular) eingefügt werden, was empfohlen wird (Ausführung täglich). Die Nutzungsbedingungen derjeweiligen Seiten sind beim Einsatz zu beachten.

## Einstellungen
Update die Parameter in den Zeilen 7 - 15 zur korrekten Einstellung des Tools.
- `url` - muss entweder [insolvenzbekanntmachungen.de](https://neu.insolvenzbekanntmachungen.de/ap/) oder [restrukturierungsbekanntmachung.de](https://www.restrukturierungsbekanntmachung.de/res-ap/) sein. 
- `company_full_name` - muss der vollständige Name sein (Groß-Kleinschreibung beachten!). Kann herausgefunden werden via Suche im [handelsregister.de](https://www.handelsregister.de/rp_web/normalesuche/welcome.xhtml).
- `found_message` und `not_found_message` sind die Texte, die bei einem Treffer und keinem Treffer im Log geschrieben werden oder in den Windows-Benachrichtigungen angezeigt werden.
- `use_windows_notifier` - wenn `True` wird eine Windows-Benachrichtigungen bei einem Treffer angezeigt.
- `use_info_to_file` - wenn `True` wird das Ergebnis (gefunden oder nicht gefunden) in ein Logfile geschrieben.
- `info_file_path` - vollständiger Pfad des Logfiles, für gefundene und nicht gefundene Einträge, sowie für Fehlermeldungen.

# English
This tool automates single requests to [insolvenzbekanntmachungen.de](https://neu.insolvenzbekanntmachungen.de/ap/) and [restrukturierungsbekanntmachung.de](https://www.restrukturierungsbekanntmachung.de/res-ap/). Results can be saved in a logfile as well as shown with the Windows Notifier. It can be used manually or implemented into the Windows Task Schedular which is recommended (daily). The TOS of the websites must be met.

## Settings
Update the following parameters in line 7 - 15 to customize your experience.
- `url` - this must be either [insolvenzbekanntmachungen.de](https://neu.insolvenzbekanntmachungen.de/ap/) or [restrukturierungsbekanntmachung.de](https://www.restrukturierungsbekanntmachung.de/res-ap/). 
- `company_full_name` - this must be the full name of your company (case sensitive), you can find the correct one by searching via [handelsregister.de](https://www.handelsregister.de/rp_web/normalesuche/welcome.xhtml).
- `found_message` and `not_found_message` this is the text displayed in the log and Windows Notifier.
- `use_windows_notifier` - if `True` this returns a Windows Notfication if something is found.
- `use_info_to_file` - if `True` this writes the output (found or not found) to a file.
- `info_file_path` - full path to the file to log the found and not found information as well as errors.


## Deployment
### Environment
This is the list of versions which were used for creation. Newer versions should work as well.
- python 3.10.2
    - requests 2.33.1
    - BeautifulSoup 3.2.2
    - for windows notification:
        - pypiwin32 223
        - setuptools 82.0.1
        - pywin32 311
        - win10toast 0.9

- Deployment via Windows Task Schedular - daily

## Other interesting links
- https://github.com/coezbek/registerbekanntmachungen 
- https://www.bundesanzeiger.de/pub/de/start?0 - published accounts
- https://github.com/bundesAPI/handelsregister - general data
