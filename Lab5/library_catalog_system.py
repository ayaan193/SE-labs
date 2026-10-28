"""Manage a library catalog, borrowed books, and CSV exports."""

import csv
import hashlib
import secrets

CATALOG = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}
OUTSTANDING_LOANS = {book_id: 0 for book_id in CATALOG}


def issue_book(book_id, patron, active_issues=None):
    """Issue a book and optionally add an entry to the activity log."""
    book = CATALOG.get(book_id)
    if book is None or book["copies"] <= 0:
        return False

    book["copies"] -= 1
    OUTSTANDING_LOANS[book_id] += 1
    if active_issues is not None:
        active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return a book only when an outstanding loan exists."""
    if book_id not in CATALOG or OUTSTANDING_LOANS[book_id] <= 0:
        return False

    CATALOG[book_id]["copies"] += 1
    OUTSTANDING_LOANS[book_id] -= 1
    return True


def check_availability(book_id):
    """Return whether an existing book has at least one available copy."""
    return CATALOG.get(book_id, {}).get("copies", 0) > 0


def calculate_fine(days_overdue, daily_rate=2.0):
    """Calculate a nonnegative fine from numeric days and a daily rate."""
    if days_overdue < 0 or daily_rate < 0:
        raise ValueError("Overdue days and daily rate cannot be negative")
    return round(days_overdue * daily_rate, 2)


def generate_patron_hash(patron_id):
    """Return a SHA-256 identifier digest (not a password hash)."""
    return hashlib.sha256(patron_id.encode("utf-8")).hexdigest()


def generate_temp_patron_pin():
    """Generate an unpredictable four-digit temporary PIN."""
    return secrets.randbelow(9000) + 1000


def export_catalog(filename="catalog_export.csv"):
    """Export book identifiers, titles, and available counts to UTF-8 CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(("book_id", "title", "copies"))
        for book_id, book in CATALOG.items():
            writer.writerow((book_id, book["title"], book["copies"]))

    print(f"Catalog backup exported to: {filename}")


def main():
    """Show the library operations without exposing generated credentials."""
    audit_log = []
    issue_book("B01", "P101", audit_log)
    print("Return without a loan:", return_book("B02"))
    print("Return borrowed B01:", return_book("B01"))
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4))
    print("Patron hash:", generate_patron_hash("P101"))
    generate_temp_patron_pin()
    print("Temporary patron PIN generated securely (value not logged)")
    print("Audit log:", audit_log)
    export_catalog()


if __name__ == "__main__":
    main()
