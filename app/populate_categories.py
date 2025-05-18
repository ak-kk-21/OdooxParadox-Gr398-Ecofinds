import sqlite3

DATABASE = 'instance/marketplace.db'

default_categories = [
    "Furniture", "Clothing", "Electronics", "Books", "Home Decor",
    "Toys", "Kitchenware", "Outdoor", "Office Supplies",
    "Crafts", "Vintage", "Tools", "Musical Instruments"
]

def populate_categories():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    for name in default_categories:
        try:
            cur.execute("INSERT INTO Categories (name) VALUES (?)", (name,))
        except sqlite3.IntegrityError:
            print(f"Category '{name}' already exists. Skipping.")

    conn.commit()
    conn.close()
    print("Categories populated successfully.")

if __name__ == "__main__":
    populate_categories()
