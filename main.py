import sqlite3
import re
import urwid

# Prompt 2: Centralized Database Connection Helper
def get_connection():
    return sqlite3.connect('contactBook.db')

# Switched places between prompt 1 and 2 for functionality
# Prompt 1: Create Database Schema
def create_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        # Emails table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY,
                contact_id INTEGER NOT NULL,
                email TEXT NOT NULL,
                FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE
            )
        ''')

        # Phones table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                id INTEGER PRIMARY KEY,
                contact_id INTEGER NOT NULL,
                phone TEXT NOT NULL,
                FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()

# Prompt 3: Add Contact with Multiple Emails and Phones
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone(phone):
    return re.match(r"^\+?[0-9]+$", phone) is not None

def add_contact(name, emails, phones):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Insert contact
            cursor.execute('INSERT INTO contacts (name) VALUES (?)', (name,))
            contact_id = cursor.lastrowid

            # Insert emails
            for email in emails:
                if validate_email(email):
                    cursor.execute('INSERT INTO emails (contact_id, email) VALUES (?, ?)', (contact_id, email))
                else:
                    print(f"Invalid email skipped: {email}")

            # Insert phones
            for phone in phones:
                if validate_phone(phone):
                    cursor.execute('INSERT INTO phones (contact_id, phone) VALUES (?, ?)', (contact_id, phone))
                else:
                    print(f"Invalid phone skipped: {phone}")

            conn.commit()
        print(f"Contact '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Prompt 4: View All Contacts
def view_contacts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, name FROM contacts')
    contacts = cursor.fetchall()

    result = []
    for contact in contacts:
        contact_id, name = contact
        emails = cursor.execute('SELECT email FROM emails WHERE contact_id = ?', (contact_id,)).fetchall()
        phones = cursor.execute('SELECT phone FROM phones WHERE contact_id = ?', (contact_id,)).fetchall()

        result.append({
            "id": contact_id,
            "name": name,
            "emails": [email[0] for email in emails],
            "phones": [phone[0] for phone in phones],
        })

    conn.close()
    return result

# Prompt 5: Search Contacts by Name, Email, or Phone
def search_contacts(search_term):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT contacts.id, contacts.name
        FROM contacts
        LEFT JOIN emails ON contacts.id = emails.contact_id
        LEFT JOIN phones ON contacts.id = phones.contact_id
        WHERE contacts.name LIKE ? OR emails.email LIKE ? OR phones.phone LIKE ?
    ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    contacts = cursor.fetchall()

    result = []
    for contact_id, name in contacts:
        emails = cursor.execute('SELECT email FROM emails WHERE contact_id = ?', (contact_id,)).fetchall()
        phones = cursor.execute('SELECT phone FROM phones WHERE contact_id = ?', (contact_id,)).fetchall()

        result.append({
            "id": contact_id,
            "name": name,
            "emails": [email[0] for email in emails],
            "phones": [phone[0] for phone in phones],
        })

    conn.close()
    return result

# Prompt 6: Class for main operations
class ContactBookApp:
    def __init__(self):
        self.loop = None
        self.menu_widget = self.menu()

    def menu(self):
        body = urwid.Text("Welcome to Contact Book!")
        buttons = [
            urwid.Button("Add Contact", self.go_to_add_contact),
            urwid.Button("View Contacts", self.go_to_view_contacts),
            urwid.Button("Search Contacts", self.go_to_search_contacts),
            urwid.Button("Delete Contact", self.go_to_delete_contact),
            urwid.Button("Exit", self.exit_program),
        ]
        pile = urwid.Pile([body] + buttons)
        return urwid.Filler(pile)

    def start(self):
        self.loop = urwid.MainLoop(self.menu_widget)
        self.loop.run()

    # Prompt 7: Add contacts with Name, Emails and Phone numbers

    def go_to_add_contact(self, button):
        name_edit = urwid.Edit("Name: ")
        emails_edit = urwid.Edit("Emails (comma-separated): ")
        phones_edit = urwid.Edit("Phones (comma-separated): ")
        save_button = urwid.Button("Save", lambda _: self.handle_add_contact(
            name_edit.edit_text,
            emails_edit.edit_text.split(','),
            phones_edit.edit_text.split(',')
        ))
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([name_edit, emails_edit, phones_edit, save_button, back_button])
        self.loop.widget = urwid.Filler(pile)

    def handle_add_contact(self, name, emails, phones):
        add_contact(name, emails, phones)
        self.return_to_menu()

    # Prompt 8: View, search & delete contacts

    def go_to_view_contacts(self, button):
        contacts = view_contacts()
        text = "\n".join(
            f"Name: {c['name']}, Emails: {', '.join(c['emails'])}, Phones: {', '.join(c['phones'])}"
            for c in contacts
        )
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([urwid.Text(text), back_button])
        self.loop.widget = urwid.Filler(pile)

    def go_to_search_contacts(self, button):
        search_edit = urwid.Edit("Enter search term (name, email, or phone): ")
        search_button = urwid.Button("Search", lambda _: self.handle_search_contacts(search_edit.edit_text))
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([search_edit, search_button, back_button])
        self.loop.widget = urwid.Filler(pile)

    def handle_search_contacts(self, search_term):
        results = search_contacts(search_term)
        if results:
            text = "\n".join(
                f"Name: {c['name']}, Emails: {', '.join(c['emails'])}, Phones: {', '.join(c['phones'])}"
                for c in results
            )
        else:
            text = "No contacts found."
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([urwid.Text(text), back_button])
        self.loop.widget = urwid.Filler(pile)

    def go_to_delete_contact(self, button):
        contact_name_edit = urwid.Edit("Enter Contact Name to delete: ")
        delete_button = urwid.Button("Delete", lambda _: self.handle_delete_contact(contact_name_edit.edit_text))
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([contact_name_edit, delete_button, back_button])
        self.loop.widget = urwid.Filler(pile)

    def handle_delete_contact(self, name):
        if name.strip():  # Ensure the name is not empty
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
                    if cursor.rowcount > 0:
                        conn.commit()
                        message = f"Contact '{name}' deleted successfully."
                    else:
                        message = f"No contact found with the name '{name}'."
            except sqlite3.Error as e:
                message = f"An error occurred: {e}"
        else:
            message = "Contact name cannot be empty."

        # Show result message and return to menu
        back_button = urwid.Button("Return to Menu", self.return_to_menu)
        pile = urwid.Pile([urwid.Text(message), back_button])
        self.loop.widget = urwid.Filler(pile)

    def return_to_menu(self, button=None):
        self.loop.widget = self.menu_widget

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

if __name__ == "__main__":
    create_database()
    app = ContactBookApp()
    app.start()
