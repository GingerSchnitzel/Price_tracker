Introducere
Aplicația "Price Tracker" este destinată monitorizării fluctuațiilor de preț ale produselor de pe eMag și trimiterea de notificări prin e-mail utilizatorilor atunci când prețul unui produs scade. Acest fișier README conține instrucțiuni detaliate pentru instalarea aplicației, configurarea mediului de dezvoltare și rularea aplicației pe serverul local Django.

1. Instalare Aplicație și Pachete Necesare

Pasul 1: Clonarea Repozitoriului
Pentru a începe, clonează repo-ul Git al aplicației pe calculatorul tău:

git clone https://github.com/username/price-tracker.git
cd price-tracker

Pasul 2: Crearea unui mediu virtual
Este recomandat să creezi un mediu virtual pentru a izola pachetele necesare aplicației. Pentru a crea și activa un mediu virtual:

Pe Windows:
python -m venv venv
venv\Scripts\activate

Pe macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Pasul 3: Instalarea dependențelor
După activarea mediului virtual, instalează toate dependențele din fișierul requirements.txt:

pip install -r requirements.txt

2. Setări de Configurare
Aplicația necesită o configurare minimă înainte de a fi rulată local.

Configurarea bazei de date: Aplicația utilizează baza de date configurată în fișierul settings.py. Asigură-te că ai setat corect conexiunea la baza de date, dacă folosești un alt tip decât SQLite (de exemplu, PostgreSQL sau MySQL).

Configurarea e-mailului: Pentru trimiterea notificărilor prin e-mail, aplicația folosește setările SMTP. Aceste setări sunt configurabile în fișierul settings.py și checker.py, iar pentru serviciile precum Gmail, trebuie să adaugi informațiile corespunzătoare pentru serverul SMTP și autentificare.

3. Configurarea Bazei de Date
Migrarea bazei de date
Pentru a crea structura bazei de date, rulează următoarele comenzi:

python manage.py migrate

Aceasta va crea tabelele necesare pentru aplicația ta în baza de date configurată.

Crearea unui Superuser
Pentru a accesa panoul de administrare Django, trebuie să creezi un superuser. Rulează următoarea comandă pentru a crea un cont de administrator:

python manage.py createsuperuser

Urmează pașii de pe ecran pentru a introduce un nume de utilizator, adresă de e-mail și parolă pentru superuser.

4. Pornirea Aplicației Local

Pornirea serverului de dezvoltare
După ce ai configurat aplicația, baze de date și setările, poți porni serverul local Django cu următoarea comandă:

python manage.py runserver

Aceasta va porni serverul la adresa http://127.0.0.1:8000/, iar aplicația va fi accesibilă din browserul tău.

5. Testarea Aplicației
Pentru a te asigura că aplicația funcționează corect:

Verifică dacă poți adăuga produse urmăribile (prin completarea formularului de adăugare produs).
Testează dacă notificările prin e-mail sunt trimise corect atunci când prețul unui produs scade.
Verifică panoul de administrare pentru a te asigura că poți vizualiza produsele și gestionarea utilizatorilor (dacă e cazul).

Concluzie
Aceste instrucțiuni te vor ghida în instalarea și configurarea aplicației Tracker de Prețuri pe sistemul tău local. Dacă întâmpini probleme, consultă secțiunea de troubleshooting din manualul de utilizare sau contactează echipa de suport.