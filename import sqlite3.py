"""Small script to dump the `organisms` table from the sqlite DB.

Note: the filename contains a space which is unusual in Python projects, but we
keep it to avoid breaking any local tooling/scripts that might reference it.
"""

from __future__ import annotations

import sqlite3


def main(db_path: str = "organism_data.db") -> None:
    """Print all rows from the `organisms` table in the given sqlite database."""
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM organisms")
            for row in cur.fetchall():
                print(row)
        finally:
            cur.close()
    finally:
        conn.close()


if __name__ == "__main__":
    main()