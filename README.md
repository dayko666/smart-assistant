# Information

Smart Assistant is a Telegram bot, a small, useful product with three main modules:
Habit Tracker
Task Planner
Financial Tracker

The bot runs on Python 3.12 and uses python-telegram-bot 21.7, with SQLite storage.
The interface is implemented using Reply Keyboard, ensuring convenient buttons are always available in the bottom chat bar.

---------

# Features:

Language
Prompt to select a language on first launch
Bilingual support: English and Russian
Ability to change languages ​​via the menu
Habits
Adding a new habit
Viewing the habit list
Marking completed actions
Tracking streaks
Setting a weekly goal
Viewing statistics
Tasks
Creating a task
Setting a due date
Viewing the task list
Marking completed tasks
Finances
Adding expenses
Adding income
Categorizing transactions
Adding comments
Summary statistics
Balance calculation

---------

# Project architecture:

The project is divided into independent modules:
common — routing, keyboards, and basic logic
habits — habits module
tasks — tasks module
finance — finance accounting module
storage — working with SQLite
texts — dictionary of all texts and a multilingual system

All modules are completely isolated and Managed through the main text messaging router.

--------

# Requirements:

Python 3.12+
Libraries from requirements.txt

---------

# Installation

Clone the repository:
git clone https://github.com/username/smart-assistant.git
cd smart-assistant
Install dependencies:
pip install -r requirements.txt
Specify the bot token in config.py:
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
Specify the admin client ID in config.py:
ADMINS = [YOUR_TELEGRAM_CLIENT_ID]
Run the bot:
python main.py

Upon first run, an SQLite database is automatically created in the db directory.

---------

# Project Structure

smart-assistant/
| main.py
| config.py
| requirements.txt
|
|---core/
| texts.py
| storage.py
|
|---handlers/
| common.py
| habits.py
| tasks.py
| finance.py
|
|---db/

---------

# Usage

Open the bot in Telegram and send the command:
/start
After selecting the language, the main menu with permanent buttons will appear.
Further interaction is carried out via the bottom keyboard bar.