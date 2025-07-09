import tkinter as tk
from tkinter import messagebox
import os
import pickle

class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age
        self.friends = []
        self.notifications = []

    def add_friend_request(self, sender):
        self.notifications.append(f"Friend request from {sender}")

    def display_info(self):
        return f":User  {self.username}, Age: {self.age}, Friends: {', '.join(self.friends) if self.friends else 'No friends yet'}"

class Post:
    def __init__(self, content, author, tags):
        self.content = content
        self.author = author
        self.tags = tags
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BuddyBoard")
        self.root.geometry("500x700")
        self.main_frame = tk.Frame(self.root, bg="#D6EAF8")  # Background color
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.users = self.load_data("users.pkl", [])
        self.posts = self.load_data("posts.pkl", [])
        self.current_user = None

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
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Welcome to BuddyBoard",
            font=("Arial", 18, "bold"),
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)
        tk.Button(
            self.main_frame,
            text="Login",
            command=self.login_screen,
            font=("Arial", 14),
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Register",
            command=self.register_screen,
            font=("Arial", 14),
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)

    def login_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Login",
            font=("Arial", 18, "bold"),
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)
        tk.Label(self.main_frame, text="Username:", bg="#D6EAF8").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:", bg="#D6EAF8").pack()
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

        tk.Button(
            self.main_frame,
            text="Login",
            command=login,
            bg="#FF6347",
            fg="white",
            width=15,
        ).pack(pady=20)

    def register_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Register",
            font=("Arial", 18, "bold "), 
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)
        tk.Label(self.main_frame, text="Username:", bg="#D6EAF8").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:", bg="#D6EAF8").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        tk.Label(self.main_frame, text="Age:", bg="#D6EAF8").pack()
        age_entry = tk.Entry(self.main_frame)
        age_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            age = age_entry.get()

            if not username or not password or not age.isdigit() or int(age) < 0:
                messagebox.showerror("Error", "Invalid input! Please ensure all fields are filled correctly.")
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

        tk.Button(
            self.main_frame,
            text="Register",
            command=register,
            bg="#FF6347",
            fg="white",
            width=15,
        ).pack(pady=20)

    def dashboard(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text=f"Welcome, {self.current_user.username}",
            font=("Arial", 18, "bold"),
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)
        tk.Button(
            self.main_frame,
            text="Create Post",
            command=self.create_post_screen,
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="View Posts",
            command=self.view_posts_screen,
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Logout",
            command=self.logout,
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)

    def create_post_screen(self):
        self.clear_frame()  # Clear previous screen

        tk.Label(
            self.main_frame,
            text="Create a Post",
            font=("Arial", 18, "bold"),
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)

        tk.Label(self.main_frame, text="Post Content:", bg="#D6EAF8").pack()
        content_entry = tk.Entry(self.main_frame, width=40)
        content_entry.pack(pady=10)

        tk.Label(self.main_frame, text="Tags (comma separated):", bg="#D6EAF8").pack()
        tags_entry = tk.Entry(self.main_frame, width=40)
        tags_entry.pack(pady=10)

        def create_post():
            content = content_entry.get()
            tags = tags_entry.get().split(",") if tags_entry.get() else []
            if content.strip():  # Ensure content is not just whitespace
                new_post = Post(content, self.current_user.username, tags)
                self.posts.append(new_post)
                self.save_data("posts.pkl", self.posts)
                messagebox.showinfo("Success", "Post created successfully!")
                self.dashboard()
            else:
                messagebox.showerror("Error", "Post content cannot be empty!")

        tk.Button(
            self.main_frame,
            text="Create Post",
            command=create_post,
            bg="#FF6347",
            fg="white",
            width=15,
        ).pack(pady=20)

    def view_posts_screen(self):
        self.clear_frame()  # Clear previous screen
        tk.Label(
            self.main_frame,
            text="Posts",
            font=("Arial", 18, "bold"),
            bg="#D6EAF8",
            fg="#FF6347",
        ).pack(pady=20)

        if not self.posts:
            messagebox.showinfo("Info", "No posts available!")
            self.dashboard()
            return

        for post in self.posts:
            post_text = f"Author: {post.author}\nTags: {', '.join(post.tags)}\n{post.content}\n{'-'*40}\n"
            tk.Label(self.main_frame, text=post_text, bg="#D6EAF8", anchor="w", justify="left").pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#FFDAB9",
            fg="black",
            width=15,
        ).pack(pady=10)

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "You have successfully logged out!")
        self.setup_gui()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaApp(root)
    root.mainloop() 