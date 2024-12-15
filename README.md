# aiContactBook

A simple terminal-based application to create and manage a digital contact book. Easily add, search, and delete contacts right from your terminal!

## Features

- **Add Contacts**: Create new contacts by name and assign multiple emails and phone numbers to each contact.
- **Search Contacts**: Quickly search through your contact list using a name, email, or phone number. Partial matches are supported by entering one letter or number.
- **Delete Contacts**: Delete a contact using their full name to prevent accidental deletions.

## Getting Started

Follow the steps below to download and start using the application.

### Prerequisites

- Ensure you have Python installed on your machine (version 3.6 or above).
- Git installed to clone the repository.

### Installation

1. **Clone the Repository**

   Open your terminal and run the following command:

   ```bash
   git clone https://github.com/hackerboy112/aiContactBook.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd aiContactBook
   ```

3. **Install Dependencies**

   Install the required Python packages using the following command:

   ```bash
   pip install -r requirements.txt
   ```

   The dependencies include:
   - **urwid==2.1.2**: A library used for building the Text User Interface (TUI) of the application.
   - **sqlite3**: Bundled with Python, used for managing the database of contacts.

### Running the Application

Run the following command to start the application:

```bash
python main.py
```

Replace `main.py` with the entry-point script of your application if it has a different name.

## Usage

- Add contacts by following the prompts in the application.
- Search contacts using a partial name, email, or phone number.
- Delete contacts by entering their full name.

## License

This project is licensed under the [MIT License](LICENSE).