# BuddyBoard

BuddyBoard is a simple social media application built with Python and Tkinter. It allows users to register, log in, create posts, and view posts from all users. The app features a user-friendly GUI, persistent data storage, and a scrollable post feed.

## Features

- **User Registration & Login:** Users can create an account and log in securely.
- **Create Posts:** Logged-in users can create posts with content and tags.
- **View Posts:** All posts are displayed in a scrollable feed, showing the author, tags, and content.
- **Persistent Storage:** User and post data are saved using Python's `pickle` module.
- **Simple, Colorful UI:** The interface uses a modern color scheme and is easy to navigate.

## Getting Started

### Prerequisites
- Python 3.x
- Tkinter (usually included with Python)

### Installation
1. **Clone or Download the Repository**
   - Place `test3.py` in your desired directory.
2. **Install Dependencies**
   - No external dependencies are required beyond Python and Tkinter.

### Running the App
1. Open a terminal or command prompt.
2. Navigate to the directory containing `test3.py`.
3. Run the following command:
   ```bash
   python test3.py
   ```

## Usage
- **Register:** Click 'Register' on the welcome screen, fill in your details, and submit.
- **Login:** Enter your username and password to log in.
- **Create Post:** After logging in, click 'Create Post' to write and submit a new post.
- **View Posts:** Click 'View Posts' to see all posts in a scrollable window.
- **Logout:** Click 'Logout' to return to the welcome screen.

## File Structure
- `test3.py` - Main application file containing all logic and GUI code.
- `users.pkl` - Stores registered user data (created automatically).
- `posts.pkl` - Stores post data (created automatically).

## Notes
- All data is stored locally using pickle files. Deleting these files will reset users and posts.
- The app is designed for educational/demo purposes and does not implement advanced security features.

## Screenshots
*Add screenshots here if desired.*

## License
This project is for educational use. Feel free to modify and use it as you wish.
