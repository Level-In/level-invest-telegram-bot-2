import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["TELEGRAM_TOKEN"]

CHAT_IDS = [
    "-1004231126426",
    "-1004249984029",
    "-1003932802265"
]

day = datetime.now(ZoneInfo("Europe/Warsaw")).weekday()

messages = {
    0: """Poniedziałek 🚀 Nowy tydzień, nowa energia

Dzień dobry! 🔥

Ruszamy mocno od samego rana. Poniedziałek nadaje tempo całemu tygodniowi, więc zaczynamy konkretnie i bez odkładania działań na później.

🎯 Priorytet dnia: telefony do klientów, obdzwonienie kontaktów z Otodom i ustawienie rozmów na kolejne kroki.

📞 Cel: jak najwięcej konkretnych rozmów, powrotów do klientów i nowych szans na spotkania.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Wchodzimy punktualnie i zaczynamy z energią 💪""",

    1: """Wtorek ⚡ Konsekwencja robi wynik

Dzień dobry! 💪

Dzisiaj kontynuujemy tempo z poniedziałku. Wynik nie bierze się z jednego mocnego dnia, tylko z powtarzalnych działań każdego dnia.

🎯 Priorytet dnia: telefony, Otodom, kontakt z klientami i powroty do osób, które już były zainteresowane.

📞 Cel: nie zostawiać rozmów bez kolejnego kroku. Każdy kontakt ma zakończyć się decyzją, terminem albo jasnym statusem.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Startujemy punktualnie 🔥""",

    2: """Środa 🔥 Połowa tygodnia, czas przyspieszyć

Dzień dobry! 📈

Jesteśmy w połowie tygodnia. To najlepszy moment, żeby sprawdzić, co już ruszyło, co trzeba dopchnąć i gdzie możemy jeszcze wyciągnąć wynik.

🎯 Priorytet dnia: powroty do klientów, obdzwonienie kontaktów z Otodom i domykanie rozmów, które są blisko decyzji.

📞 Cel: wrócić do tematów, które czekają na odpowiedź, i zamienić zainteresowanie w konkretny kolejny krok.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Widzimy się punktualnie 💪""",

    3: """Czwartek 💼 Weekend blisko, teraz trzeba docisnąć

Dzień dobry! 🔥

Weekend już się zbliża, ale to właśnie teraz nie można odpuszczać. Czwartek to dzień na przyspieszenie i dopilnowanie tematów, które mogą jeszcze wejść przed końcem tygodnia.

🎯 Priorytet dnia: telefony, kontakt z klientami, Otodom i pilnowanie spraw blisko decyzji.

📞 Cel: ruszyć tematy, które stoją w miejscu, i uzyskać jasny status od klientów.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Działamy punktualnie ⚡""",

    4: """Piątek ✅ Dopięcie tematów przed weekendem

Dzień dobry! 🏁

Dzisiaj domykamy tydzień. Piątek to dzień na uporządkowanie spraw, kontakt z właścicielami i przekazanie im konkretnych informacji o statusie ich mieszkań.

🎯 Priorytet dnia: kontakt z właścicielami, statusy mieszkań, telefony do klientów i domknięcie najważniejszych rozmów.

🏡 Cel: każdy właściciel powinien dostać jasną informację, co dzieje się z jego nieruchomością.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Zaczynamy punktualnie 💪""",

    5: """Sobota 🏆 Dla najbardziej ambitnych

Dzień dobry! 🔥

Sobota jest dla tych, którzy chcą zrobić więcej niż reszta. To dobry moment na odświeżenie kontaktów, telefony i ruszenie tematów, które mogą dać przewagę na kolejny tydzień.

🎯 Priorytet dnia: telefony, powroty do klientów, odświeżenie kontaktów i dopięcie spraw, które można jeszcze ruszyć.

📞 Cel: zrobić konkretne rozmowy i zostawić po sobie efekt, zanim zacznie się nowy tydzień.

⏰ Google Meet o 9:30
https://meet.google.com/psa-rxvd-fba

Proszę się nie spóźniać. Ambitni zaczynają punktualnie 🚀"""
}

MESSAGE = messages.get(day)

if not MESSAGE:
    print("Niedziela, brak wysyłki")
    exit()

for chat_id in CHAT_IDS:
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": MESSAGE
        }
    )
    print(chat_id, response.status_code, response.text)
