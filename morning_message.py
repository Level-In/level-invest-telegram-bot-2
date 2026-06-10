```python
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests


TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("Błąd: brak zmiennej środowiskowej TELEGRAM_TOKEN")
    sys.exit(1)


CHAT_IDS = [
    "-1004231126426",
    "-1004249984029",
    "-1003932802265",
]


MEET_LINK = "https://meet.google.com/psa-rxvd-fba"


MESSAGES = {
    0: f"""Poniedziałek 🚀 Nowy tydzień, nowa energia

Dzień dobry! 🔥

Ruszamy mocno od samego rana. Poniedziałek nadaje tempo całemu tygodniowi, więc zaczynamy konkretnie i bez odkładania działań na później.

🎯 Priorytet dnia:
telefony do klientów, obdzwonienie kontaktów z Otodom i ustawienie rozmów na kolejne kroki.

📞 Cel:
jak najwięcej konkretnych rozmów, powrotów do klientów i nowych szans na spotkania.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Wchodzimy punktualnie i zaczynamy z energią 💪""",

    1: f"""Wtorek ⚡ Konsekwencja robi wynik

Dzień dobry! 💪

Dzisiaj kontynuujemy tempo z poniedziałku. Wynik nie bierze się z jednego mocnego dnia, tylko z powtarzalnych działań każdego dnia.

🎯 Priorytet dnia:
telefony, Otodom, kontakt z klientami i powroty do osób, które już były zainteresowane.

📞 Cel:
nie zostawiać rozmów bez kolejnego kroku. Każdy kontakt ma zakończyć się decyzją, terminem albo jasnym statusem.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Startujemy punktualnie 🔥""",

    2: f"""Środa 🔥 Połowa tygodnia, czas przyspieszyć

Dzień dobry! 📈

Jesteśmy w połowie tygodnia. To najlepszy moment, żeby sprawdzić, co już ruszyło, co trzeba dopchnąć i gdzie możemy jeszcze wyciągnąć wynik.

🎯 Priorytet dnia:
powroty do klientów, obdzwonienie kontaktów z Otodom i domykanie rozmów, które są blisko decyzji.

📞 Cel:
wrócić do tematów, które czekają na odpowiedź, i zamienić zainteresowanie w konkretny kolejny krok.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Widzimy się punktualnie 💪""",

    3: f"""Czwartek 💼 Weekend blisko, teraz trzeba docisnąć

Dzień dobry! 🔥

Weekend już się zbliża, ale to właśnie teraz nie można odpuszczać. Czwartek to dzień na przyspieszenie i dopilnowanie tematów, które mogą jeszcze wejść przed końcem tygodnia.

🎯 Priorytet dnia:
telefony, kontakt z klientami, Otodom i pilnowanie spraw blisko decyzji.

📞 Cel:
ruszyć tematy, które stoją w miejscu, i uzyskać jasny status od klientów.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Działamy punktualnie ⚡""",

    4: f"""Piątek ✅ Dopięcie tematów przed weekendem

Dzień dobry! 🏁

Dzisiaj domykamy tydzień. Piątek to dzień na uporządkowanie spraw, kontakt z właścicielami i przekazanie im konkretnych informacji o statusie ich mieszkań.

🎯 Priorytet dnia:
kontakt z właścicielami, statusy mieszkań, telefony do klientów i domknięcie najważniejszych rozmów.

🏡 Cel:
każdy właściciel powinien dostać jasną informację, co dzieje się z jego nieruchomością.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Zaczynamy punktualnie 💪""",

    5: f"""Sobota 🏆 Dla najbardziej ambitnych

Dzień dobry! 🔥

Sobota jest dla tych, którzy chcą zrobić więcej niż reszta. To dobry moment na odświeżenie kontaktów, telefony i ruszenie tematów, które mogą dać przewagę na kolejny tydzień.

🎯 Priorytet dnia:
telefony, powroty do klientów, odświeżenie kontaktów i dopięcie spraw, które można jeszcze ruszyć.

📞 Cel:
zrobić konkretne rozmowy i zostawić po sobie efekt, zanim zacznie się nowy tydzień.

⏰ Google Meet o 9:30
{MEET_LINK}

Proszę się nie spóźniać. Ambitni zaczynają punktualnie 🚀""",
}


def send_telegram_message(chat_id: str, message: str) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, data=payload, timeout=15)
        response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            print(f"Wysłano do {chat_id}")
            return True

        print(f"Błąd Telegrama dla {chat_id}: {result}")
        return False

    except requests.exceptions.RequestException as error:
        print(f"Błąd wysyłki do {chat_id}: {error}")
        return False


def main() -> None:
    today = datetime.now(ZoneInfo("Europe/Warsaw")).weekday()
    message = MESSAGES.get(today)

    if not message:
        print("Niedziela, brak wysyłki")
        return

    success_count = 0

    for chat_id in CHAT_IDS:
        if send_telegram_message(chat_id, message):
            success_count += 1

    print(f"Zakończono. Wysłano poprawnie: {success_count}/{len(CHAT_IDS)}")


if __name__ == "__main__":
    main()
```
