import os
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


# --------------------------------------------------
# FETCH DATA FROM NOTION
# --------------------------------------------------

def fetch_books():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

    books = []
    payload = {}

    while True:
        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()
        books.extend(data["results"])

        if not data.get("has_more"):
            break

        payload["start_cursor"] = data["next_cursor"]

    return books


# --------------------------------------------------
# NOTION PROPERTY HELPERS
# --------------------------------------------------

def get_text(property_data):
    items = property_data.get("rich_text", [])

    if not items:
        return None

    return "".join(item["plain_text"] for item in items)


def get_title(property_data):
    items = property_data.get("title", [])

    if not items:
        return None

    return "".join(item["plain_text"] for item in items)


def clean_label(value):
    """
    Removes leading emojis/symbols.

    Examples:
    ✅ Finished -> Finished
    🦄 Fantasy -> Fantasy
    👩‍🏫 Currently Reading -> Currently Reading
    """
    if not value:
        return value

    value = value.strip()

    while value and not value[0].isalnum():
        value = value[1:]

    return value.strip()


# --------------------------------------------------
# CONVERT NOTION BOOK -> NORMAL PYTHON DICTIONARY
# --------------------------------------------------

def parse_book(book):
    properties = book["properties"]

    status_property = properties["Status"]["select"]
    language_property = properties["Language"]["select"]
    dates_read = properties["Dates Read"]["date"]

    date_started = None
    date_finished = None

    if dates_read:
        date_started = dates_read.get("start")
        date_finished = dates_read.get("end")

    status = None
    if status_property:
        status = clean_label(status_property["name"])

    language = None
    if language_property:
        language = clean_label(language_property["name"])

    genres = [
        clean_label(genre["name"])
        for genre in properties["Genre"]["multi_select"]
    ]

    cover_url = properties["Cover Formula"]["formula"].get("string")

    # Fallback to the Book Cover property if needed
    if not cover_url:
        cover_files = properties["Book Cover"]["files"]

        if cover_files:
            first_cover = cover_files[0]

            if first_cover["type"] == "external":
                cover_url = first_cover["external"]["url"]
            elif first_cover["type"] == "file":
                cover_url = first_cover["file"]["url"]

    return {
        "title": get_title(properties["Title"]),
        "author": get_text(properties["Author"]),
        "series": get_text(properties["Buchreihe"]),
        "status": status,
        "date_started": date_started,
        "date_finished": date_finished,
        "total_pages": properties["Total Pages"]["number"],
        "pages_read": properties["Pages Read"]["number"],
        "progress": properties["Progress"]["formula"]["number"],
        "rating": properties["My Rating"]["number"],
        "genres": genres,
        "language": language,
        "duration_days": properties["Duration (Days)"]["formula"]["number"],
        "cover_url": cover_url,
        "isbn": get_text(properties["ISBN"]),
    }


def get_books():
    raw_books = fetch_books()

    return [
        parse_book(book)
        for book in raw_books
    ]


# --------------------------------------------------
# FILTERING
# --------------------------------------------------

def get_finished_books_for_year(books, year):
    finished_books = []

    for book in books:
        if not book["date_finished"]:
            continue

        finished_year = int(book["date_finished"][:4])

        if finished_year == year:
            finished_books.append(book)

    return finished_books


def get_current_books(books):
    current_books = []

    for book in books:
        if book["status"] == "Currently Reading":
            current_books.append(book)

    current_books.sort(
        key=lambda book: book["date_started"] or "",
        reverse=True,
    )

    return current_books


def get_recent_books(books, limit=5):
    finished_books = [
        book
        for book in books
        if book["date_finished"]
    ]

    finished_books.sort(
        key=lambda book: book["date_finished"],
        reverse=True,
    )

    return finished_books[:limit]


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

def get_yearly_stats(books):
    books_read = len(books)

    page_values = [
        book["total_pages"]
        for book in books
        if book["total_pages"] is not None
    ]

    ratings = [
        book["rating"]
        for book in books
        if book["rating"] is not None
    ]

    pages_read = sum(page_values)

    average_length = 0
    if page_values:
        average_length = round(
            pages_read / len(page_values)
        )

    average_rating = None
    if ratings:
        average_rating = round(
            sum(ratings) / len(ratings),
            2,
        )

    longest_book = None
    shortest_book = None

    books_with_pages = [
        book
        for book in books
        if book["total_pages"] is not None
    ]

    if books_with_pages:
        longest_book = max(
            books_with_pages,
            key=lambda book: book["total_pages"],
        )

        shortest_book = min(
            books_with_pages,
            key=lambda book: book["total_pages"],
        )

    return {
        "books_read": books_read,
        "pages_read": pages_read,
        "average_length": average_length,
        "average_rating": average_rating,
        "longest_book": longest_book,
        "shortest_book": shortest_book,
    }


def get_monthly_book_counts(books):
    monthly_counts = {
        month: 0
        for month in range(1, 13)
    }

    for book in books:
        if not book["date_finished"]:
            continue

        month = int(book["date_finished"][5:7])

        monthly_counts[month] += 1

    return monthly_counts


def get_monthly_page_counts(books):
    monthly_pages = {
        month: 0
        for month in range(1, 13)
    }

    for book in books:
        if not book["date_finished"]:
            continue

        if book["total_pages"] is None:
            continue

        month = int(book["date_finished"][5:7])

        monthly_pages[month] += book["total_pages"]

    return monthly_pages


# --------------------------------------------------
# DISPLAY HELPERS
# --------------------------------------------------

MONTH_NAMES = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember",
}


def format_number(number):
    """
    8436 -> 8.436
    """
    return f"{number:,}".replace(",", ".")


def format_rating(rating):
    if rating is None:
        return "Keine Bewertung"

    rounded = round(rating)

    full_stars = "★" * rounded
    empty_stars = "☆" * (5 - rounded)

    number = str(rating).replace(".", ",")

    return f"{full_stars}{empty_stars} ({number} / 5)"


def format_date(date_string):
    if not date_string:
        return ""

    date = datetime.strptime(
        date_string[:10],
        "%Y-%m-%d",
    )

    return date.strftime("%d.%m.%Y")

def get_best_books(books, limit=30):
    best_books = [
        book
        for book in books
        if book["rating"] == 5
    ]

    best_books.sort(
        key=lambda book: book["date_finished"] or "",
        reverse=True,
    )

    return best_books[:limit]

def get_reading_years(books):
    years = set()

    for book in books:
        if not book["date_finished"]:
            continue

        year = int(
            book["date_finished"][:4]
        )

        years.add(year)

    return sorted(
        years,
        reverse=True,
    )

def get_monthly_book_chart(monthly_counts):
    lines = []

    max_month_length = max(
        len(name)
        for name in MONTH_NAMES.values()
    )

    for month, count in monthly_counts.items():
        month_name = MONTH_NAMES[month]

        bar = "█" * count

        lines.append(
            f"{month_name:<{max_month_length}}  "
            f"{bar:<12} {count}"
        )

    return lines

def get_reading_years(books):
    years = set()

    for book in books:
        if not book["date_finished"]:
            continue

        year = int(
            book["date_finished"][:4]
        )

        years.add(year)

    return sorted(
        years,
        reverse=True,
    )
# --------------------------------------------------
# MARKDOWN GENERATION
# --------------------------------------------------


def reading_years_markdown(years):
    lines = [
        "## Lesejahre",
        "",
    ]

    for year in years:
        lines.append(
            f"- [{year}](/blog/reading/{year}/)"
        )

    return "\n".join(lines)


def current_books_markdown(books):
    lines = [
        "## Aktuell lese ich",
        "",
    ]

    if not books:
        lines.append("Momentan lese ich kein Buch.")
        return "\n".join(lines)

    for book in books:
        lines.append(
            f"### {book['title']} — {book['author']}"
        )
        lines.append("")

        if book["cover_url"]:
            lines.append(
                f"![Cover von {book['title']}]({book['cover_url']})"
            )
            lines.append("")

        if book["pages_read"] is not None and book["total_pages"]:
            lines.append(
                f"**Fortschritt:** "
                f"{book['pages_read']} von "
                f"{book['total_pages']} Seiten"
            )
            lines.append("")

        if book["progress"] is not None:
            percentage = round(book["progress"] * 100)
            lines.append(f"**Gelesen:** {percentage} %")
            lines.append("")

        if book["date_started"]:
            lines.append(
                f"**Begonnen:** {format_date(book['date_started'])}"
            )

        lines.append("")

    return "\n".join(lines)

def recent_books_markdown(books):
    lines = [
        "## Zuletzt gelesen",
        "",
    ]

    for book in books:
        lines.append(
            f"### {book['title']} — {book['author']}"
        )
        lines.append("")

        if book["cover_url"]:
            lines.append(
                f"![Cover von {book['title']}]"
                f"({book['cover_url']})"
            )
            lines.append("")

        lines.append(
            f"**Bewertung:** "
            f"{format_rating(book['rating'])}"
        )
        lines.append("")

        lines.append(
            f"**Beendet:** "
            f"{format_date(book['date_finished'])}"
        )

        if book["total_pages"] is not None:
            lines.append("")
            lines.append(
                f"**Seiten:** {book['total_pages']}"
            )

        if book["series"]:
            lines.append("")
            lines.append(
                f"**Buchreihe:** {book['series']}"
            )

        lines.append("")

    return "\n".join(lines)


def yearly_stats_markdown(stats):
    lines = [
        "## Mein Lesejahr in Zahlen",
        "",
        f"- **Gelesene Bücher:** {stats['books_read']}",
        (
            f"- **Gelesene Seiten:** "
            f"{format_number(stats['pages_read'])}"
        ),
        (
            f"- **Durchschnittliche Buchlänge:** "
            f"{stats['average_length']} Seiten"
        ),
    ]

    if stats["average_rating"] is not None:
        average_rating = str(
            stats["average_rating"]
        ).replace(".", ",")

        lines.append(
            f"- **Durchschnittliche Bewertung:** "
            f"{average_rating} von 5"
        )

    longest = stats["longest_book"]

    if longest:
        lines.append(
            f"- **Längstes Buch:** "
            f"{longest['title']} — "
            f"{longest['total_pages']} Seiten"
        )

    shortest = stats["shortest_book"]

    if shortest:
        lines.append(
            f"- **Kürzestes Buch:** "
            f"{shortest['title']} — "
            f"{shortest['total_pages']} Seiten"
        )

    return "\n".join(lines)


def monthly_books_markdown(monthly_counts):
    lines = [
        "## Bücher pro Monat",
        "",
        "```",
    ]

    lines.extend(
        get_monthly_book_chart(monthly_counts)
    )

    lines.append("```")

    return "\n".join(lines)

def get_monthly_page_chart(monthly_pages):
    lines = []

    max_month_length = max(
        len(name)
        for name in MONTH_NAMES.values()
    )

    max_pages = max(monthly_pages.values())

    max_bar_length = 20

    for month, pages in monthly_pages.items():
        month_name = MONTH_NAMES[month]

        if max_pages > 0:
            bar_length = round(
                pages / max_pages * max_bar_length
            )
        else:
            bar_length = 0

        bar = "█" * bar_length

        lines.append(
            f"{month_name:<{max_month_length}}  "
            f"{bar:<20} "
            f"{format_number(pages)}"
        )

    return lines

def monthly_pages_markdown(monthly_pages):
    lines = [
        "## Gelesene Seiten pro Monat",
        "",
        "```",
    ]

    lines.extend(
        get_monthly_page_chart(monthly_pages)
    )

    lines.append("```")

    return "\n".join(lines)


def bookshelf_markdown(books, year):
    lines = [
        f"## Mein Bücherregal {year}",
        "",
    ]

    sorted_books = sorted(
        books,
        key=lambda book: book["date_finished"],
    )

    for index, book in enumerate(
        sorted_books,
        start=1,
    ):
        lines.append(
            f"{index}. "
            f"{book['title']} — "
            f"{book['author']} — "
            f"{format_rating(book['rating'])}"
        )

    return "\n".join(lines)


def generate_reading_markdown(books, year):
    books_for_year = get_finished_books_for_year(
        books,
        year,
    )

    best_books = get_best_books(
        books_for_year,
        limit=30,
    )

    stats = get_yearly_stats(
        books_for_year
    )

    monthly_counts = get_monthly_book_counts(
        books_for_year
    )

    monthly_pages = get_monthly_page_counts(
        books_for_year
    )

    sections = [
        f"# Mein Lesejahr {year}",
        "",
        f"Mein Lesejahr {year} in Büchern und Zahlen.",
        "",
        best_books_markdown(
            best_books,
            year,
        ),
        "",
        yearly_stats_markdown(stats),
        "",
        monthly_books_markdown(monthly_counts),
        "",
        monthly_pages_markdown(monthly_pages),
        "",
        bookshelf_markdown(
            books_for_year,
            year,
        ),
        "",
        "[← Zurück zur Leseübersicht](/blog/reading/)",
        "",
        "[← Zurück zum Blog](/)",
    ]

    return "\n".join(sections)

def best_books_markdown(books, year):
    lines = [
        f"## Meine besten Bücher {year}",
        "",
    ]

    if not books:
        lines.append(
            "Bisher gibt es noch keine Bücher mit 5 von 5 Sternen."
        )
        return "\n".join(lines)

    for book in books:
        lines.append(
            f"### {book['title']} — {book['author']}"
        )
        lines.append("")

        if book["cover_url"]:
            lines.append(
                f"![Cover von {book['title']}]"
                f"({book['cover_url']})"
            )
            lines.append("")

        lines.append(
            f"**Bewertung:** {format_rating(book['rating'])}"
        )
        lines.append("")

        if book["date_finished"]:
            lines.append(
                f"**Beendet:** "
                f"{format_date(book['date_finished'])}"
            )
            lines.append("")

        if book["series"]:
            lines.append(
                f"**Buchreihe:** {book['series']}"
            )
            lines.append("")

    return "\n".join(lines)

def write_reading_index(books):
    output_path = "content/blog/reading/index.md"

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    markdown = generate_reading_index_markdown(
        books
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(markdown)

    print(
        f"Generated reading index: {output_path}"
    )

def write_reading_page(
    books,
    year,
    output_path=None,
):
    if output_path is None:
        output_path = (
            f"content/blog/reading/{year}/index.md"
        )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    markdown = generate_reading_markdown(
        books,
        year,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(markdown)

    print(
        f"Generated reading page: {output_path}"
    )


def generate_reading_index_markdown(books):
    current_books = get_current_books(books)

    recent_books = get_recent_books(
        books,
        limit=5,
    )

    years = get_reading_years(books)

    sections = [
        "# Meine Bücher",
        "",
        (
            "Hier sammle ich, was ich gerade lese, "
            "welche Bücher zuletzt auf meinem Stapel "
            "lagen und meine Lesejahre in Zahlen."
        ),
        "",
        current_books_markdown(current_books),
        "",
        recent_books_markdown(recent_books),
        "",
        "## Rezensionen",
        "",
        (
            "Nicht jedes Buch bekommt eine ausführliche Rezension. "
            "Aber manchmal bleiben nach der letzten Seite noch ein paar "
            "Gedanken übrig, die ich festhalten möchte."
        ),
        "",
        "[→ Zu meinen Buchrezensionen](/blog/reading/reviews/)",
        "",
        reading_years_markdown(years),
        "",
        "[← Zurück zum Blog](/)",
    ]

    return "\n".join(sections)

# --------------------------------------------------
# RUN DIRECTLY
# --------------------------------------------------
def generate_all_reading_pages():
    print("Fetching books from Notion...")

    books = get_books()

    print(
        f"Fetched {len(books)} books"
    )

    write_reading_index(books)

    years = get_reading_years(books)

    for year in years:
        write_reading_page(
            books,
            year,
        )

    print(
        f"Generated reading pages for "
        f"{len(years)} years"
    )
if __name__ == "__main__":
    generate_all_reading_pages()