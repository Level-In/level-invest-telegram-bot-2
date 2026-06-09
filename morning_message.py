```python
import os
import sys
import argparse
import requests
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# KONFIGURACJA GŁÓWNA
# ============================================================

START_DATE = date.fromisoformat("2026-06-10")
SCHEDULE_DAYS = 360

TIMEZONE = ZoneInfo("Europe/Warsaw")

CHAT_IDS = [
    "-1004231126426",
    "-1004249984029",
    "-1003932802265",
]

MEET_LINK = "https://meet.google.com/psa-rxvd-fba"

REQUEST_TIMEOUT_SECONDS = 20


# ============================================================
# NAZWY DNI I TEKSTY ROTACYJNE
# ============================================================

WEEKDAY_NAMES = {
    0: "Poniedziałek",
    1: "Wtorek",
    2: "Środa",
    3: "Czwartek",
    4: "Piątek",
    5: "Sobota",
    6: "Niedziela",
}

SALES_THOUGHTS = [
    "Klient częściej podejmuje decyzję, gdy ma jasny następny krok.",
    "Najlepszy sprzedawca nie mówi najwięcej, tylko najlepiej prowadzi rozmowę.",
    "Follow up nie jest przypominaniem się, tylko prowadzeniem procesu.",
    "W sprzedaży wygrywa ten, kto szybciej wraca do klienta z konkretem.",
    "Rozmowa bez ustalonego kolejnego kroku najczęściej nie prowadzi do wyniku.",
    "Cena bez informacji zwrotnej z rynku jest tylko założeniem.",
    "Właściciel powinien dostać fakty, nie ogólne wrażenia.",
    "Każda odmowa przybliża do rozmowy, która zakończy się konkretem.",
    "Aktywność od rana daje przewagę nad tymi, którzy dopiero się rozpędzają.",
    "Nie chodzi o to, żeby zadzwonić raz. Chodzi o to, żeby prowadzić temat do decyzji.",
    "Pewność w rozmowie bierze się z przygotowania, nie z przypadku.",
    "Im szybciej reagujesz na zainteresowanie klienta, tym większa szansa na wynik.",
    "Dobre pytanie często sprzedaje lepiej niż długi monolog.",
    "Sprzedaż to proces. Każda rozmowa powinna przesuwać temat do przodu.",
    "Odmowa nie kończy procesu. Często pokazuje, czego klient naprawdę potrzebuje.",
    "Właściciel łatwiej podejmuje decyzję, gdy widzi liczby i reakcję rynku.",
    "Najlepszy follow up jest konkretny: status, propozycja i następny krok.",
    "Nie zostawiaj klienta z ogólną informacją. Daj mu kierunek działania.",
    "Telefon wykonany od razu ma większą wartość niż idealny plan bez działania.",
    "Sprzedaż rośnie wtedy, gdy codziennie pilnujesz małych działań.",
    "Klient kupuje poczucie bezpieczeństwa, nie tylko samą ofertę.",
    "Właściciel chce wiedzieć, co dalej. Naszą rolą jest prowadzić proces.",
    "Skuteczność zaczyna się od liczby rozmów, ale wynik od jakości prowadzenia tematu.",
    "Każdy kontakt bez statusu wraca później jako zaległość.",
    "Nie czekaj, aż klient sam wróci. Prowadź rozmowę do decyzji.",
    "Najlepsze okazje często pojawiają się po drugim albo trzecim kontakcie.",
    "Rynek daje informację zwrotną codziennie. Trzeba ją zebrać i przekazać właścicielowi.",
    "Dobra rozmowa telefoniczna ma cel, strukturę i konkretny finał.",
    "Jeżeli temat stoi, potrzebuje decyzji, nie kolejnego odkładania.",
    "Sprzedaż telefoniczna premiuje szybkość, systematyczność i pewność w rozmowie.",
]

OPENINGS = [
    "Dzisiaj działamy konkretnie od rana. Każdy telefon i każda rozmowa może otworzyć nowy temat.",
    "Wchodzimy w dzień z energią i jasnym celem. Liczy się aktywność, tempo i konsekwencja.",
    "Dzisiaj nie czekamy na wynik. Budujemy go rozmowami, follow upem i szybkim działaniem.",
    "Zaczynamy mocno. Im szybciej ruszymy z kontaktami, tym więcej szans stworzymy w ciągu dnia.",
    "Dzisiaj skupiamy się na konkretach. Mniej odkładania, więcej rozmów i decyzji.",
    "Dobry dzień sprzedażowy zaczyna się od pierwszego telefonu. Ruszamy z tematem od razu.",
    "Dzisiaj liczy się tempo. Każdy kontakt ma przybliżyć nas do decyzji, spotkania albo pozyskania.",
    "Nie zostawiamy aktywności na później. Zaczynamy od rozmów, które mogą dać realny wynik.",
    "Dzisiaj pracujemy blisko klienta i właściciela. Konkrety, statusy i następne kroki.",
    "W sprzedaży nieruchomości liczy się szybka reakcja. Dzisiaj wykorzystujemy każdą okazję.",
]

SALES_ELEMENTS = [
    "telefony do klientów",
    "telefony do właścicieli",
    "obdzwonienie kontaktów z Otodom",
    "follow up po rozmowach",
    "umawianie spotkań",
    "domykanie decyzji",
    "pozyskiwanie mieszkań na wynajem",
    "pozyskiwanie mieszkań na sprzedaż",
    "praca na liczbach",
    "ustalanie kolejnego kroku po każdej rozmowie",
    "informowanie właścicieli o statusie nieruchomości",
    "powroty do starych kontaktów",
    "szybka reakcja na zainteresowanie klienta",
    "rozmowy z osobami decyzyjnymi",
    "praca z odmową",
    "odświeżanie tematów",
    "pilnowanie ofert",
    "szukanie nowych okazji",
    "budowanie relacji z klientem",
    "rozmowy o cenie i reakcji rynku",
]


# ============================================================
# REGUŁY DNI TYGODNIA
# ============================================================

WEEKDAY_RULES = {
    0: {
        "emoji": "🚀",
        "theme": "Mocny start tygodnia",
        "priority_templates": [
            "telefony, Otodom, pozyskiwanie mieszkań i umawianie rozmów z właścicielami",
            "plan działań, kontakty z właścicielami i szybkie uruchomienie nowych tematów",
            "aktywność od rana, nowe leady i pozyskiwanie mieszkań na wynajem oraz sprzedaż",
            "rozmowy z właścicielami, nowe oferty i ustawienie tempa na cały tydzień",
            "telefony do klientów, powroty do leadów i rozpoczęcie tygodnia od konkretów",
        ],
        "goal_templates": [
            "ustawić tempo tygodnia i rozpocząć jak najwięcej konkretnych rozmów",
            "każdą rozmowę zakończyć decyzją, terminem albo jasnym statusem",
            "zbudować bazę tematów, które będziemy prowadzić przez cały tydzień",
            "ruszyć nowe kontakty i nie odkładać pierwszych telefonów na później",
            "zebrać konkretne szanse sprzedażowe i pozyskowe już od rana",
        ],
    },
    1: {
        "emoji": "⚡",
        "theme": "Konsekwencja robi wynik",
        "priority_templates": [
            "follow up, powroty do klientów, rozmowy z właścicielami i pilnowanie statusów",
            "praca na liczbach, telefony i doprowadzanie rozmów do kolejnego kroku",
            "odświeżenie tematów z poniedziałku i kontakt z osobami decyzyjnymi",
            "sprawdzenie wszystkich rozmów rozpoczętych wczoraj i dopchnięcie ich dalej",
            "kontynuacja tempa, Otodom, telefony i jasne statusy po każdej rozmowie",
        ],
        "goal_templates": [
            "nie zostawić żadnej rozmowy bez następnego kroku",
            "wrócić do rozpoczętych tematów i przesunąć je bliżej decyzji",
            "utrzymać tempo i dołożyć kolejne konkretne rozmowy do wyniku tygodnia",
            "zamienić luźne zainteresowanie w spotkanie, decyzję albo konkretny termin",
            "dopilnować, żeby każdy kontakt miał przypisany kolejny krok",
        ],
    },
    2: {
        "emoji": "🔥",
        "theme": "Połowa tygodnia, czas przyspieszyć",
        "priority_templates": [
            "kontrola wyniku, powroty do tematów blisko decyzji i domykanie kolejnych kroków",
            "analiza aktywności, Otodom i rozmowy, które mogą przejść w spotkania",
            "zwiększenie liczby telefonów i dopchnięcie tematów, które stoją w miejscu",
            "sprawdzenie, które rozmowy mają potencjał i szybki powrót z konkretem",
            "domykanie tematów rozpoczętych na początku tygodnia i praca na liczbach",
        ],
        "goal_templates": [
            "zamienić zainteresowanie w spotkanie, decyzję albo konkretny status",
            "sprawdzić, co działa, i przyspieszyć tam, gdzie jest największa szansa na wynik",
            "wrócić do rozmów, które są blisko decyzji, i nie zostawiać ich bez prowadzenia",
            "wyciągnąć z połowy tygodnia jasny obraz wyniku i listę tematów do domknięcia",
            "zwiększyć aktywność tam, gdzie brakuje rozmów albo statusów",
        ],
    },
    3: {
        "emoji": "💼",
        "theme": "Dociśnięcie przed końcówką tygodnia",
        "priority_templates": [
            "leady, rozmowy z klientami, kontakt z właścicielami i sprawy blisko decyzji",
            "Otodom, telefony, właściciele i szybkie ustalanie statusów",
            "aktywność sprzedażowa, pilnowanie ofert i przygotowanie do piątkowego domykania",
            "rozmowy, które mogą jeszcze wejść przed końcem tygodnia",
            "kontakt z klientami i właścicielami, którzy potrzebują konkretnego następnego kroku",
        ],
        "goal_templates": [
            "wyciągnąć jasny status z każdej rozmowy i nie zostawiać spraw w zawieszeniu",
            "przygotować tematy do piątkowego domykania i kontaktu właścicielskiego",
            "ruszyć maksymalnie dużo spraw, zanim tydzień zacznie się zamykać",
            "doprowadzić najważniejsze rozmowy do decyzji albo terminu kolejnego kontaktu",
            "przygotować właścicielskie statusy i listę tematów do zamknięcia",
        ],
    },
    4: {
        "emoji": "✅",
        "theme": "Domykamy tydzień i informujemy właścicieli",
        "priority_templates": [
            "kontakt z właścicielami, statusy nieruchomości, telefony i domykanie rozmów",
            "przekazanie właścicielom konkretów oraz uporządkowanie tematów przed weekendem",
            "informacja zwrotna z rynku, rozmowy z właścicielami i decyzje cenowe",
            "podsumowanie aktywności, statusy ofert i rozmowy o dalszym kierunku",
            "kontakt z właścicielami, jakość zainteresowania i rekomendacja dalszego działania",
        ],
        "goal_templates": [
            "każdy właściciel ma dostać jasną informację, co dzieje się z jego nieruchomością",
            "przekazać fakty, zaproponować kierunek i nie zostawiać tematów bez decyzji",
            "domknąć tydzień konkretnym statusem dla klientów i właścicieli",
            "zostawić po tygodniu porządek, status i ustalony dalszy kierunek",
            "przekazać właścicielom liczby, jakość zapytań i rekomendację działania",
        ],
    },
    5: {
        "emoji": "🏆",
        "theme": "Dzień dla ambitnych",
        "priority_templates": [
            "odświeżenie kontaktów, powroty do klientów i dopięcie spraw, które można jeszcze ruszyć",
            "dodatkowe telefony, stare kontakty i przygotowanie przewagi na kolejny tydzień",
            "nadrabianie rozmów, szybkie follow upy i domykanie tematów przed nowym tygodniem",
            "kontakt z osobami, które nie odpowiedziały w tygodniu, i odświeżenie tematów",
            "dodatkowa aktywność, stare leady, powroty i przygotowanie listy na poniedziałek",
        ],
        "goal_templates": [
            "wykonać konkretne rozmowy i zostawić po sobie efekt przed nowym tygodniem",
            "ruszyć sprawy, które w tygodniu nie dostały odpowiedzi",
            "zrobić przewagę wtedy, gdy większość rynku zwalnia tempo",
            "wejść w kolejny tydzień z gotowymi tematami i lepszym statusem kontaktów",
            "zamknąć to, co można zamknąć, i przygotować to, co trzeba poprowadzić dalej",
        ],
    },
}


# ============================================================
# ŚWIĘTA
# ============================================================

def easter_sunday(year: int) -> date:
    """
    Oblicza Wielkanoc dla kalendarza gregoriańskiego.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day_number = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day_number)


def polish_holidays(year: int) -> dict[date, str]:
    """
    Święta stałe, ruchome oraz Wigilia traktowana jako dzień wolny.
    """
    easter = easter_sunday(year)

    return {
        date(year, 1, 1): "Nowy Rok",
        date(year, 1, 6): "Trzech Króli",
        easter: "Wielkanoc",
        easter + timedelta(days=1): "Poniedziałek Wielkanocny",
        date(year, 5, 1): "Święto Pracy",
        date(year, 5, 3): "Święto Konstytucji 3 Maja",
        easter + timedelta(days=49): "Zielone Świątki",
        easter + timedelta(days=60): "Boże Ciało",
        date(year, 8, 15): "Wniebowzięcie Najświętszej Maryi Panny i Święto Wojska Polskiego",
        date(year, 11, 1): "Wszystkich Świętych",
        date(year, 11, 11): "Święto Niepodległości",
        date(year, 12, 24): "Wigilia Bożego Narodzenia",
        date(year, 12, 25): "Boże Narodzenie",
        date(year, 12, 26): "Drugi dzień Świąt Bożego Narodzenia",
    }


def special_days(year: int) -> dict[date, str]:
    """
    Dni specjalne, które nie zawsze są dniami ustawowo wolnymi,
    ale warto je obsłużyć innym tonem.
    """
    return {
        date(year, 12, 31): "Sylwester",
    }


def get_holidays_for_range(start: date, days: int) -> dict[date, str]:
    end = start + timedelta(days=days)
    all_days = {}

    for year in range(start.year, end.year + 1):
        all_days.update(polish_holidays(year))
        all_days.update(special_days(year))

    return {
        day: name
        for day, name in all_days.items()
        if start <= day < end
    }


# ============================================================
# FUNKCJE KALENDARZOWE
# ============================================================

def first_workday_of_month(day: date, holidays: dict[date, str]) -> date:
    current = date(day.year, day.month, 1)

    while current.weekday() == 6 or current in holidays:
        current += timedelta(days=1)

    return current


def last_workdays_of_month(day: date, holidays: dict[date, str], count: int = 5) -> list[date]:
    if day.month == 12:
        current = date(day.year, 12, 31)
    else:
        current = date(day.year, day.month + 1, 1) - timedelta(days=1)

    workdays = []

    while len(workdays) < count:
        if current.weekday() != 6 and current not in holidays:
            workdays.append(current)
        current -= timedelta(days=1)

    return sorted(workdays)


def is_day_before_holiday(day: date, holidays: dict[date, str]) -> str | None:
    tomorrow = day + timedelta(days=1)
    return holidays.get(tomorrow)


def upcoming_holiday_within_days(day: date, holidays: dict[date, str], days: int = 3) -> tuple[date, str] | None:
    for offset in range(1, days + 1):
        checked_day = day + timedelta(days=offset)
        if checked_day in holidays:
            return checked_day, holidays[checked_day]
    return None


def recent_holiday_within_days(day: date, holidays: dict[date, str], days: int = 4) -> tuple[date, str] | None:
    for offset in range(1, days + 1):
        checked_day = day - timedelta(days=offset)
        if checked_day in holidays:
            return checked_day, holidays[checked_day]
    return None


def is_may_weekend_period(day: date) -> bool:
    return day.month == 5 and 1 <= day.day <= 5


def is_christmas_period(day: date) -> bool:
    return day.month == 12 and 20 <= day.day <= 31


def is_easter_period(day: date) -> bool:
    easter = easter_sunday(day.year)
    return easter - timedelta(days=3) <= day <= easter + timedelta(days=2)


def is_long_weekend_context(day: date, holidays: dict[date, str]) -> bool:
    """
    Wykrywa krótszy tydzień albo okres z obniżoną dostępnością klientów.
    """
    if is_may_weekend_period(day):
        return True

    if is_christmas_period(day):
        return True

    if is_easter_period(day):
        return True

    if upcoming_holiday_within_days(day, holidays, days=2):
        return True

    if recent_holiday_within_days(day, holidays, days=2):
        return True

    return False


def is_extra_activity_sunday(day: date, holidays: dict[date, str]) -> bool:
    """
    Niedziela z wysyłką tylko wtedy, gdy trzeba nadrobić aktywność po świętach
    albo przed krótszym tygodniem.
    """
    if day.weekday() != 6:
        return False

    if is_long_weekend_context(day, holidays):
        return True

    recent = recent_holiday_within_days(day, holidays, days=4)
    upcoming = upcoming_holiday_within_days(day, holidays, days=4)

    if recent:
        return True

    if upcoming and upcoming[0].weekday() < 5:
        return True

    return False


# ============================================================
# GENEROWANIE TREŚCI
# ============================================================

def pick(items: list[str], day: date, salt: int = 0) -> str:
    """
    Deterministyczny wybór tekstu.
    Ta sama data zawsze dostanie tę samą wersję.
    """
    index = (day.toordinal() + salt) % len(items)
    return items[index]


def meet_block() -> str:
    return (
        f"⏰ Google Meet o 9:30\n"
        f"{MEET_LINK}\n\n"
        f"Proszę się nie spóźniać. Startujemy punktualnie."
    )


def owner_block(day: date) -> str:
    variants = [
        (
            "🏡 Blok właścicielski:\n"
            "Dzisiaj informujemy właścicieli o statusie ich nieruchomości.\n"
            "Przekazujemy konkrety: liczba zapytań, liczba rozmów, jakość zainteresowania i informacja zwrotna z rynku.\n\n"
            "Jeżeli nieruchomość nie ma wystarczającego zainteresowania, proponujemy właścicielowi decyzję: "
            "obniżka ceny, załącznik nr 8 albo czekamy dalej na obecnych warunkach.\n"
            "Właściciel wybiera kierunek, a zespół prowadzi proces dalej."
        ),
        (
            "🏡 Blok właścicielski:\n"
            "Dzisiaj każdy właściciel powinien dostać jasny status swojej nieruchomości.\n"
            "Mówimy konkretnie: ile było zapytań, ile rozmów, jaka była jakość zainteresowania i co mówi rynek.\n\n"
            "Jeżeli zainteresowanie jest za słabe, dajemy właścicielowi trzy kierunki: "
            "obniżka ceny, załącznik nr 8 albo dalsze oczekiwanie na obecnych warunkach.\n"
            "Decyzja należy do właściciela, a my prowadzimy proces dalej."
        ),
        (
            "🏡 Blok właścicielski:\n"
            "Piątek to dzień konkretnej informacji dla właścicieli.\n"
            "Przekazujemy liczby, jakość zapytań, reakcję klientów i realną informację zwrotną z rynku.\n\n"
            "Jeżeli oferta nie pracuje wystarczająco dobrze, proponujemy decyzję: "
            "obniżka ceny, załącznik nr 8 albo pozostanie przy obecnych warunkach.\n"
            "Nie zostawiamy właściciela bez rekomendacji."
        ),
    ]

    return pick(variants, day, salt=50)


def standard_message(day: date) -> str | None:
    weekday = day.weekday()

    if weekday == 6:
        return None

    rule = WEEKDAY_RULES[weekday]
    weekday_name = WEEKDAY_NAMES[weekday]

    opening = pick(OPENINGS, day, salt=1)
    priority = pick(rule["priority_templates"], day, salt=2)
    goal = pick(rule["goal_templates"], day, salt=3)
    thought = pick(SALES_THOUGHTS, day, salt=4)
    greeting_emoji = pick(["🔥", "💪", "📈", "⚡", "🚀", "🏡", "📞"], day, salt=5)

    parts = [
        f"{weekday_name} {rule['emoji']} {rule['theme']}",
        "",
        f"Dzień dobry! {greeting_emoji}",
        "",
        opening,
        "",
        "🎯 Priorytet dnia:",
        priority + ".",
        "",
        "📞 Cel:",
        goal + ".",
    ]

    if weekday == 4:
        parts.extend(["", owner_block(day)])

    parts.extend([
        "",
        "💡 Sprzedażowa myśl dnia:",
        thought,
        "",
        meet_block(),
    ])

    return "\n".join(parts)


def holiday_message(day: date, holiday_name: str) -> str:
    weekday_name = WEEKDAY_NAMES[day.weekday()]
    thought = pick([
        "Dobra energia i spokojna głowa pomagają wrócić do rozmów z większą skutecznością.",
        "Odpoczynek też jest częścią dobrej pracy, jeśli po nim wracamy z konkretnym planem.",
        "Najlepsze wyniki robi zespół, który umie złapać balans i wrócić do działania z energią.",
        "Po spokojnym dniu warto wrócić do procesu z jasnym celem i konkretnym następnym krokiem.",
        "Dobra regeneracja pomaga później prowadzić rozmowy z większą koncentracją.",
    ], day, salt=60)

    return (
        f"{weekday_name} ✨ {holiday_name}\n\n"
        f"Dzień dobry! 🌿\n\n"
        f"Dzisiaj mamy dzień świąteczny, więc życzę Wam spokoju, dobrej energii i chwili oddechu.\n\n"
        f"Niech ten dzień da trochę resetu, żeby wrócić do rozmów z klientami i właścicielami z nową siłą. 💛\n\n"
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )


def pre_holiday_message(day: date, holiday_name: str) -> str:
    weekday_name = WEEKDAY_NAMES[day.weekday()]
    element_1 = pick(SALES_ELEMENTS, day, salt=10)
    element_2 = pick(SALES_ELEMENTS, day, salt=11)
    thought = pick(SALES_THOUGHTS, day, salt=12)

    return (
        f"{weekday_name} ⚡ Dzień przed świętem: {holiday_name}\n\n"
        f"Dzień dobry! 🔥\n\n"
        f"Przed dniem wolnym klienci i właściciele mogą być mniej dostępni, dlatego dzisiaj działamy szybciej i konkretniej.\n\n"
        f"🎯 Priorytet dnia:\n"
        f"{element_1}, {element_2} i domknięcie spraw, które nie powinny czekać na kolejny dzień roboczy.\n\n"
        f"📞 Cel:\n"
        f"wykonać więcej telefonów, wrócić do klientów i ustalić jasne statusy przed przerwą.\n\n"
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )


def long_weekend_message(day: date, context_name: str) -> str:
    weekday_name = WEEKDAY_NAMES[day.weekday()]
    thought = pick(SALES_THOUGHTS, day, salt=70)

    return (
        f"{weekday_name} 🚀 Krótszy tydzień, większa aktywność\n\n"
        f"Dzień dobry! 🔥\n\n"
        f"{context_name} może ograniczyć dostępność klientów i właścicieli, dlatego dzisiaj liczy się szybsze działanie i większa liczba kontaktów.\n\n"
        f"🎯 Priorytet dnia:\n"
        f"telefony, follow up, Otodom, rozmowy z właścicielami i domykanie statusów, zanim tematy przejdą na później.\n\n"
        f"📞 Cel:\n"
        f"zrobić więcej rozmów niż zwykle i nie zostawić aktywnych tematów bez decyzji albo kolejnego kroku.\n\n"
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )


def month_start_message(day: date) -> str:
    weekday_name = WEEKDAY_NAMES[day.weekday()]
    thought = pick(SALES_THOUGHTS, day, salt=20)

    return (
        f"{weekday_name} 🚀 Start miesiąca i nowy cel pozyskowy\n\n"
        f"Dzień dobry! 🔥\n\n"
        f"Zaczynamy nowy miesiąc. Od pierwszego dnia liczy się tempo, konsekwencja i liczba konkretnych rozmów.\n\n"
        f"🎯 Priorytet dnia:\n"
        f"telefony do właścicieli, Otodom, nowe kontakty i budowanie bazy mieszkań do wynajmu oraz sprzedaży.\n\n"
        f"📞 Cel:\n"
        f"minimum 15 do 20 mieszkań na wynajem lub sprzedaż w tym miesiącu. Dzisiaj pracujemy na liczbie telefonów, "
        f"liczbie rozmów z właścicielami, liczbie konkretnych ofert, liczbie pozyskanych mieszkań i tempie działania.\n\n"
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )


def month_end_message(day: date, is_last_workday: bool) -> str:
    weekday_name = WEEKDAY_NAMES[day.weekday()]
    thought = pick(SALES_THOUGHTS, day, salt=30)

    if is_last_workday:
        title = "Ostatni dzień roboczy miesiąca"
        intro = "Dzisiaj nie zostawiamy tematów bez decyzji. Końcówka miesiąca wymaga konkretu, statusu i jasnego kierunku."
        goal = "domknąć maksymalnie dużo rozmów, przekazać właścicielom statusy i zamknąć tematy bez odkładania ich na kolejny miesiąc"
    else:
        title = "Końcówka miesiąca, przyspieszamy"
        intro = "Jesteśmy w ostatnich dniach roboczych miesiąca. To moment na większą aktywność i pilnowanie każdego tematu."
        goal = "przyspieszyć rozmowy, wrócić do klientów, domykać decyzje i pilnować statusów właścicielskich"

    message = (
        f"{weekday_name} 🔥 {title}\n\n"
        f"Dzień dobry! 📈\n\n"
        f"{intro}\n\n"
        f"🎯 Priorytet dnia:\n"
        f"wynajem, sprzedaż, follow up, kontakt z właścicielami i decyzje, które mogą wejść jeszcze w tym miesiącu.\n\n"
        f"📞 Cel:\n"
        f"{goal}.\n\n"
    )

    if day.weekday() == 4:
        message += owner_block(day) + "\n\n"

    message += (
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )

    return message


def extra_sunday_message(day: date) -> str:
    thought = pick(SALES_THOUGHTS, day, salt=40)

    return (
        f"Niedziela 🚀 Dodatkowa aktywność po krótszym tygodniu\n\n"
        f"Dzień dobry! 🔥\n\n"
        f"Przez dni wolne tydzień sprzedażowy jest krótszy, więc dzisiaj warto nadrobić aktywność i przygotować przewagę na kolejne dni.\n\n"
        f"🎯 Priorytet dnia:\n"
        f"odświeżenie kontaktów, dodatkowe telefony, szybkie follow upy i przygotowanie tematów do dalszego prowadzenia.\n\n"
        f"📞 Cel:\n"
        f"wykonać kilka konkretnych rozmów i wejść w kolejny dzień z gotowym planem działania.\n\n"
        f"💡 Sprzedażowa myśl dnia:\n"
        f"{thought}\n\n"
        f"{meet_block()}"
    )


def get_long_weekend_context(day: date, holidays: dict[date, str]) -> str | None:
    if is_may_weekend_period(day):
        return "Majówka skraca tydzień sprzedażowy"

    if is_christmas_period(day):
        return "Okres świąteczno noworoczny skraca rytm pracy"

    if is_easter_period(day):
        return "Okres wielkanocny skraca dostępność klientów"

    upcoming = upcoming_holiday_within_days(day, holidays, days=2)
    if upcoming:
        return f"Nadchodzący dzień wolny, {upcoming[1]}, skraca tydzień sprzedażowy"

    recent = recent_holiday_within_days(day, holidays, days=2)
    if recent:
        return f"Ostatni dzień wolny, {recent[1]}, skrócił tydzień sprzedażowy"

    return None


def get_message_for_date(day: date) -> str | None:
    """
    Główna funkcja decyzyjna.
    Priorytet:
    1. Święto
    2. Dzień przedświąteczny
    3. Początek miesiąca
    4. Końcówka miesiąca
    5. Piątek właścicielski
    6. Standardowy dzień tygodnia
    """
    if day < START_DATE:
        print(f"System startuje od {START_DATE.isoformat()}. Dzisiaj jeszcze brak wysyłki.")
        return None

    day_index = (day - START_DATE).days

    if day_index >= SCHEDULE_DAYS:
        print("Harmonogram 360 dni zakończony. Brak wiadomości do wysyłki.")
        return None

    holidays = get_holidays_for_range(START_DATE, SCHEDULE_DAYS)

    if day in holidays:
        return holiday_message(day, holidays[day])

    upcoming_holiday = is_day_before_holiday(day, holidays)
    if upcoming_holiday and day.weekday() != 6:
        return pre_holiday_message(day, upcoming_holiday)

    if day.weekday() == 6:
        if is_extra_activity_sunday(day, holidays):
            return extra_sunday_message(day)

        print("Niedziela, brak standardowej wysyłki.")
        return None

    if day == first_workday_of_month(day, holidays):
        return month_start_message(day)

    ending_days = last_workdays_of_month(day, holidays, count=5)
    if day in ending_days:
        return month_end_message(day, is_last_workday=(day == ending_days[-1]))

    long_weekend_context = get_long_weekend_context(day, holidays)
    if long_weekend_context:
        return long_weekend_message(day, long_weekend_context)

    return standard_message(day)


# ============================================================
# TELEGRAM
# ============================================================

def get_telegram_token() -> str:
    """
    Token pobieramy dopiero przy realnej wysyłce.
    Dzięki temu podgląd wiadomości działa bez tokena.
    """
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        raise RuntimeError("Brak TELEGRAM_TOKEN w zmiennych środowiskowych.")

    return token


def send_message_to_chat(chat_id: str, message: str, token: str) -> bool:
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(
            api_url,
            data={
                "chat_id": chat_id,
                "text": message,
                "disable_web_page_preview": True,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        print(f"CHAT_ID={chat_id} STATUS={response.status_code} RESPONSE={response.text}")

        if response.status_code != 200:
            return False

        payload = response.json()
        return bool(payload.get("ok"))

    except requests.exceptions.RequestException as error:
        print(f"CHAT_ID={chat_id} REQUEST_ERROR={error}")
        return False

    except ValueError as error:
        print(f"CHAT_ID={chat_id} JSON_ERROR={error}")
        return False


def send_to_all_chats(message: str, dry_run: bool = False) -> None:
    if dry_run:
        print("DRY_RUN=true, wiadomość nie zostanie wysłana.")
        print("=" * 80)
        print(message)
        print("=" * 80)
        return

    try:
        token = get_telegram_token()
    except RuntimeError as error:
        print(error)
        sys.exit(1)

    success_count = 0

    for chat_id in CHAT_IDS:
        if send_message_to_chat(chat_id, message, token):
            success_count += 1

    print(f"Wysłano poprawnie do {success_count}/{len(CHAT_IDS)} grup.")


# ============================================================
# PODGLĄD
# ============================================================

def preview_message(preview_date: date) -> None:
    message = get_message_for_date(preview_date)

    print("=" * 80)
    print(f"PODGLĄD WIADOMOŚCI NA DATĘ: {preview_date.isoformat()}")
    print("=" * 80)

    if message:
        print(message)
    else:
        print("Brak wiadomości na tę datę.")

    print("=" * 80)


def preview_range(start_day: date, days: int) -> None:
    print("=" * 80)
    print(f"PODGLĄD HARMONOGRAMU OD {start_day.isoformat()} PRZEZ {days} DNI")
    print("=" * 80)

    for offset in range(days):
        checked_day = start_day + timedelta(days=offset)
        message = get_message_for_date(checked_day)

        print("\n" + "#" * 80)
        print(f"DATA: {checked_day.isoformat()}   DZIEŃ: {WEEKDAY_NAMES[checked_day.weekday()]}")
        print("#" * 80)

        if message:
            print(message)
        else:
            print("Brak wysyłki.")

    print("\n" + "=" * 80)
    print("KONIEC PODGLĄDU")
    print("=" * 80)


# ============================================================
# ARGUMENTY I START
# ============================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatyczne wiadomości Telegram dla zespołu sprzedażowego nieruchomości."
    )

    parser.add_argument(
        "--date",
        help="Data w formacie YYYY-MM-DD. Domyślnie dzisiejsza data w Europe/Warsaw.",
        default=None,
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Pokazuje wiadomość w konsoli i nic nie wysyła.",
    )

    parser.add_argument(
        "--preview-range",
        type=int,
        default=None,
        help="Pokazuje harmonogram na podaną liczbę dni bez wysyłki, na przykład 14, 30 albo 360.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Pokazuje dzisiejszą wiadomość w konsoli i nic nie wysyła.",
    )

    return parser.parse_args()


def resolve_current_day(date_argument: str | None) -> date:
    if date_argument:
        try:
            return date.fromisoformat(date_argument)
        except ValueError:
            print("Błędny format daty. Użyj YYYY-MM-DD, na przykład 2026-06-10.")
            sys.exit(1)

    return datetime.now(TIMEZONE).date()


def main() -> None:
    args = parse_args()
    current_day = resolve_current_day(args.date)

    if args.preview_range is not None:
        if args.preview_range <= 0:
            print("preview-range musi być większe od 0.")
            sys.exit(1)

        preview_range(current_day, args.preview_range)
        return

    if args.preview:
        preview_message(current_day)
        return

    message = get_message_for_date(current_day)

    if not message:
        print("Brak wiadomości do wysyłki na dzisiejszy dzień.")
        return

    send_to_all_chats(message, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
```
