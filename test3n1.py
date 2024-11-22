import tkinter as tk
from tkinter import messagebox
import pickle

# User class
class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age
        self.friends = []
        self.notifications = []
        self.friend_requests = []

    def add_friend_request(self, sender):
        self.friend_requests.append(sender)

    def accept_friend_request(self, sender):
        if sender not in self.friends:
            self.friends.append(sender)
            return True
        return False

    def display_info(self):
        return f"User: {self.username}, Age: {self.age}, Friends: {', '.join(self.friends) if self.friends else 'No friends yet'}"

# Post class
class Post:
    def __init__(self, content, author, tags, visibility="Public"):
        self.content = content
        self.author = author
        self.tags = tags
        self.comments = []
        self.visibility = visibility  # Can be "Public" or "Friends"

    def add_comment(self, comment):
        self.comments.append(comment)

# Social Media App
class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BUDDY BOARD") 

        # Load data
        self.users = self.load_data("users.pkl", [])
        self.posts = self.load_data("posts.pkl", [])
        self.current_user = None

        # GUI setup
        self.setup_gui()

    def save_data(self, filename, data):
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    def load_data(self, filename, default):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return default

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Initial screen: Login or Register
        tk.Label(self.main_frame, text="Welcome to the BUDDYBOARD", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Login", command=self.login_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Register", command=self.register_screen).pack(pady=5)

    def login_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Username:").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()

            for user in self.users:
                if user.username == username and user.password == password:
                    self.current_user = user
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    self.dashboard()
                    return
            messagebox.showerror("Error", "Invalid username or password!")

        tk.Button(self.main_frame, text="Login", command=login).pack(pady=10)

    def register_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Username:").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        tk.Label(self.main_frame, text="Age:").pack()
        age_entry = tk.Entry(self.main_frame)
        age_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            age = age_entry.get()

            if not username or not password or not age.isdigit():
                messagebox.showerror("Error", "Invalid input!")
                return

            for user in self.users:
                if user.username == username:
                    messagebox.showerror("Error", "Username already exists!")
                    return

            new_user = User(username, password, int(age))
            self.users.append(new_user)
            self.save_data("users.pkl", self.users)
            messagebox.showinfo("Success", "Registration successful!")
            self.login_screen()

        tk.Button(self.main_frame, text="Register", command=register).pack(pady=10)

    def dashboard(self):
        self.clear_frame()

        tk.Label(self.main_frame, text=f"Welcome, {self.current_user.username}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Create Post", command=self.create_post_screen).pack(pady=5)
        tk.Button(self.main_frame, text="View Posts", command=self.view_posts_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Friend Requests", command=self.friend_requests_screen).pack(pady=5)
        tk.Button(self.main_frame, text="View Notifications", command=self.notifications_screen).pack(pady=5)
        tk.Button(self.main_frame, text="View Friends", command=self.view_friends).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def view_friends(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Friends List", font=("Arial", 16)).pack(pady=10)
        for friend in self.current_user.friends:
            tk.Label(self.main_frame, text=friend).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    def create_post_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Create Post", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Content:").pack()
        content_entry = tk.Entry(self.main_frame)
        content_entry.pack()

        tk.Label(self.main_frame, text="Tags (comma-separated):").pack()
        tags_entry = tk.Entry(self.main_frame)
        tags_entry.pack()

        visibility_var = tk.StringVar(value="Public")
        tk.Label(self.main_frame, text="Visibility:").pack()
        tk.Radiobutton(self.main_frame, text="Public", variable=visibility_var, value="Public").pack()
        tk.Radiobutton(self.main_frame, text="Friends", variable=visibility_var, value="Friends").pack()

        def create_post():
            content = content_entry.get()
            tags = tags_entry.get()
            visibility = visibility_var.get()

            if content and tags:
                post = Post(content, self.current_user.username, tags.split(","), visibility)
                self.posts.append(post)
                self.save_data("posts.pkl", self.posts)
                messagebox.showinfo("Success", "Post created!")
                self.dashboard()
            else:
                messagebox.showerror("Error", "Content and tags are required!")

        tk.Button(self.main_frame, text="Post", command=create_post).pack(pady=10)

    def view_posts_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Posts", font=("Arial", 16)).pack(pady=10)
        for post in self.posts:
            if post.visibility == "Public" or post.author in self.current_user.friends:
                tk.Label(self.main_frame, text=f"Author: {post.author}\nTags: {', '.join(post.tags)}\nContent: {post.content}\n").pack(pady=5)

        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    def friend_requests_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Friend Requests", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="Enter friend's username:").pack()
        friend_entry = tk.Entry(self.main_frame)
        friend_entry.pack()

        def send_request():
            friend_name = friend_entry.get()
            for user in self.users:
                if user.username == friend_name:
                    user.add_friend_request(self.current_user.username)
                    self.save_data("users.pkl", self.users)
                    messagebox.showinfo("Success", "Friend request sent!")
                    self.dashboard()
                    return
            messagebox.showerror("Error", "User not found!")

        def accept_request(friend_name):
            if self.current_user.accept_friend_request(friend_name):
                for user in self.users:
                    if user.username == friend_name:
                        user.friends.append(self.current_user.username)
                        self.save_data("users.pkl", self.users)
                        messagebox.showinfo("Success", f"Friend request from {friend_name} accepted!")
                        break
            else:
                messagebox.showinfo("Error", "Friend already added.")

        for request in self.current_user.friend_requests:
            tk.Button(self.main_frame, text=f"Accept {request}", command=lambda r=request: accept_request(r)).pack(pady=5)

        tk.Button(self.main_frame, text="Send Request", command=send_request).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    def notifications_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Notifications", font=("Arial", 16)).pack(pady=10)
        for notification in self.current_user.notifications:
            tk.Label(self.main_frame, text=notification).pack()

        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "You have successfully logged out!")
        self.setup_gui()


# Run the application
root = tk.Tk()
app = SocialMediaApp(root)
root.mainloop()
