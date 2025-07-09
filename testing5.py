import tkinter as tk
from PIL import Image, ImageTk
import pickle
class User:
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age
        self.friends = []  # List of friends
        self.friend_requests = []  # List of pending friend requests
        self.notifications = []  # List of notifications
        self.liked_posts = set()  # Set of liked post id

    def add_friend_request(self, sender):
        if sender not in self.friend_requests and sender not in self.friends:
            self.friend_requests.append(sender)

    def add_notification(self, message):
        self.notifications.append(message)

    def display_info(self):
        return f"User: {self.username}, Age: {self.age}, Friends: {', '.join(self.friends) if self.friends else 'No friends yet'}"

class Post:
    def __init__(self, content, author, tags):
        self.content = content
        self.author = author
        self.tags = tags
        self.comments = []
        self.likes = 0  # Track the number of likes
        self.liked_by = set()  # Set of users who have liked the post

    def add_comment(self, comment):
        self.comments.append(comment)

class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BuddyBoard")
        self.root.geometry("1024x768")
        self.main_frame = tk.Frame(self.root, bg="#F0F8FF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Load logo image
        self.logo_image = Image.open(r"C:/Users/PC/Downloads/BuddyBoard.jpeg")
        self.logo_image = self.logo_image.resize((50, 50), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.users=[] 
        self.posts=[] 
        self.users = self.load_data("users.pkl",list)
        self.posts = self.load_data("posts.pkl",list)  
        self.current_user = None

        self.setup_gui()


    def save_data(self, filename, data):
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    def load_data(self, filename, default):
        try:
            with open(filename, "rb") as file:
                data = pickle.load(file)
            if filename == "users.pkl":
                for user in data:
                    if not hasattr(user, "friend_requests"):
                        user.friend_requests = []
                    if not hasattr(user, "liked_posts"):
                        user.liked_posts = set()
            if filename == "posts.pkl":
                for post in data:
                    if not hasattr(post, "likes"):
                        post.likes = 0
                    if not hasattr(post, "liked_by"):
                        post.liked_by = set()
            return data
        except FileNotFoundError:
            return default

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def setup_gui(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,text="Welcome to BuddyBoard",font=("Arial", 24, "bold"),bg="#2980B9",fg="white",).pack(fill=tk.X, pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Button(
            self.main_frame,text="Login",command=self.login_screen,font=("Arial", 14),bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)
        tk.Button(
            self.main_frame,text="Register",command=self.register_screen,font=("Arial", 14),bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)

    def login_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Login",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Label(self.main_frame, text="Username:", bg="#F0F8FF").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:", bg="#F0F8FF").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            for user in self.users:
                if user.username == username and user.password == password:
                    self.current_user = user
                    tk.messagebox.showinfo("Success", f"Welcome, {user.username}!")
                    self.dashboard()
                    return
            tk.messagebox.showerror("Error", "Invalid username or password!")

        tk.Button(
            self.main_frame,
            text="Login",
            command=login,
            bg="#2E86C1",
            fg="white",
            width=15,
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.setup_gui,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=10)

    def register_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Register",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Label(self.main_frame, text="Username:", bg="#F0F8FF").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

        tk.Label(self.main_frame, text="Password:", bg="#F0F8FF").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        tk.Label(self.main_frame, text="Age:", bg="#F0F8FF").pack()
        age_entry = tk.Entry(self.main_frame)
        age_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            age = age_entry.get()
            #checking for username or pw left blank or age is something else other than numbers through isdigit() 
            if not username or not password or not age.isdigit():
                tk.messagebox.showerror("Error", "Invalid input!")
                return

            for user in self.users:
                if user.username == username:
                    tk.messagebox.showerror("Error", "Username already exists!")
                    return

            new_user = User(username, password, age)

            self.users.append(new_user)
            self.save_data("users.pkl", self.users)
            tk.messagebox.showinfo("Success", "Registration successful!")
            self.login_screen()

        tk.Button(
            self.main_frame,
            text="Register",
            command=register,
            bg="#2E86C1",
            fg="white",
            width=15,
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.setup_gui,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=10)

    def dashboard(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text=f"Welcome, {self.current_user.username}",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Create Post",
            command=self.create_post_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="View Posts",
            command=self.view_posts_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Friend Requests",
            command=self.friend_requests_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Send Friend Request",
            command=self.send_friend_request_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Notifications",
            command=self.notifications_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Friend List",
            command=self.friend_list_screen,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Logout",
            command=self.logout,
            bg="#AED6F1",
            fg="#2C3E50",
            width=20,
        ).pack(pady=10)

    def create_post_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Create a Post",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Label(self.main_frame, text="Post Content:", bg="#F0F8FF").pack()
        content_entry = tk.Entry(self.main_frame, width=50)
        content_entry.pack(pady=10)

        tk.Label(self.main_frame, text="Tags (#xyz):", bg="#F0F8FF").pack()
        tags_entry = tk.Entry(self.main_frame, width=50)
        tags_entry.pack(pady=10)

        def create_post():
            content = content_entry.get()
            tags = tags_entry.get().split(",")
            if content:
                new_post = Post(content, self.current_user.username, tags)
                self.posts.append(new_post)
                self.save_data("posts.pkl", self.posts)
                # Notify friends
                for friend in self.current_user.friends:
                    for user in self.users:
                        if user.username == friend:
                            user.add_notification(f"New post by {self.current_user.username}: {content}")
                            break
                self.save_data("users.pkl", self.users)
                tk.messagebox.showinfo("Success", "Post created successfully!")
                self.dashboard()
            else:
                tk.messagebox.showerror("Error", "Post content cannot be empty!")

        tk.Button(
            self.main_frame,
            text="Create Post",
            command=create_post,
            bg="#2E86C1",
            fg="white",
            width=20,
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=10)

    def view_posts_screen(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Posts",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        canvas = tk.Canvas(self.main_frame, bg="#F0F8FF")
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F0F8FF")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.posts:
            tk.Label(scrollable_frame, text="No posts available.", bg="#F0F8FF").pack()
        else:
            for post in self.posts:
                post_frame = tk.Frame(scrollable_frame, bg="#FFFFFF", bd=1, relief="solid")
                post_frame.pack(pady=5, padx=10, fill="x")
                tk.Label(post_frame, text=f"Author: {post.author}", bg="#FFFFFF", font=("Arial", 12, "bold")).pack(pady=2, padx=5)
                tk.Label(post_frame, text=f"Tags: {', '.join(post.tags)}", bg="#FFFFFF", font=("Arial", 10)).pack(pady=2, padx=5)
                tk.Label(post_frame, text=post.content, bg="#FFFFFF", font=("Arial", 12), wraplength=500).pack(pady=2, padx=5)
                tk.Label(post_frame, text=f"Likes: {post.likes}", bg="#FFFFFF", font=("Arial", 10)).pack(pady=2, padx=5)

                def like_post(post=post):
                    if post in self.current_user.liked_posts:
                        tk.messagebox.showerror("Error", "You have already liked this post!")
                        return
                    post.likes+=1
                    post.liked_by.add(self.current_user.username)
                    self.current_user.liked_posts.add(post)
                    self.save_data("posts.pkl", self.posts)
                    for user in self.users:
                        if user.username == post.author:
                            user.add_notification(f"{self.current_user.username} liked your post.")
                            self.save_data("users.pkl", self.users)
                            break
                    tk.messagebox.showinfo("Success", "You liked the post!")
                    self.view_posts_screen()

                tk.Button(
                    post_frame,
                    text="Like",
                    command=like_post,
                    bg="#2ECC71",
                    fg="white",
                    font=("Arial", 10),
                    width=10,
                ).pack(side="left", padx=5)

                def add_comment(post=post):
                    comment_window = tk.Toplevel(self.root)
                    comment_window.title("Add Comment")
                    tk.Label(comment_window, text="Comment:", font=("Arial", 12)).pack(pady=5)
                    comment_entry = tk.Entry(comment_window, width=50)
                    comment_entry.pack(pady=5)
                    def submit_comment():
                        comment = comment_entry.get()
                        if comment:
                            post.add_comment(f"{self.current_user.username}: {comment}")
                            self.save_data("posts.pkl", self.posts)
                            for user in self.users:
                                if user.username == post.author:
                                    user.add_notification(f"{self.current_user.username} commented on your post.")
                                    self.save_data("users.pkl", self.users)
                                    break
                            tk.messagebox.showinfo("Success", "Comment added!")
                            comment_window.destroy()
                            self.view_posts_screen()
                        else:
                            tk.messagebox.showerror("Error", "Comment cannot be empty!")
                    tk.Button(comment_window, text="Submit", command=submit_comment, bg="#3498DB", fg="white", font=("Arial", 10)).pack(pady=5)

                tk.Button(
                    post_frame,
                    text="Comment",
                    command=add_comment,
                    bg="#3498DB",
                    fg="white",
                    font=("Arial", 10),
                    width=10,
                ).pack(side="left", padx=5)

                for comment in post.comments:
                    tk.Label(post_frame, text=comment, bg="#FFFFFF", font=("Arial", 10), wraplength=500, anchor="w").pack(pady=2, padx=5)

                if post.author == self.current_user.username:
                    tk.Button(
                        post_frame,
                        text="Delete Post",
                        command=lambda p=post: self.delete_post(p),
                        bg="#FF6347",
                        fg="white",
                        font=("Arial", 10),
                        width=10,
                    ).pack(side="right", padx=5)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=20)

    def delete_post(self, post):
        self.posts.remove(post)
        self.save_data("posts.pkl", self.posts)
        tk.messagebox.showinfo("Success", "Post deleted successfully!")
        self.view_posts_screen()

    def friend_requests_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Friend Requests",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        if not self.current_user.friend_requests:
            tk.Label(self.main_frame, text="No friend requests.", bg="#F0F8FF").pack()
        else:
            for request in self.current_user.friend_requests:
                request_frame = tk.Frame(self.main_frame, bg="#F0F8FF", bd=1, relief="solid")
                request_frame.pack(pady=5, padx=10, fill="x")
                tk.Label(request_frame, text=f"Request from: {request}", bg="#F0F8FF").pack(pady=2, padx=5)

                tk.Button(
                    request_frame,
                    text="Accept",
                    command=lambda r=request: self.accept_friend_request(r),
                    bg="#2ECC71",
                    fg="white",
                    width=10,
                ).pack(side="left", padx=5)

                tk.Button(
                    request_frame,
                    text="Reject",
                    command=lambda r=request: self.reject_friend_request(r),
                    bg="#E74C3C",
                    fg="white",
                    width=10,
                ).pack(side="right", padx=5)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=20)

    def send_friend_request_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Send Friend Request",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)

        tk.Label(self.main_frame, text="Enter Username:", bg="#F0F8FF").pack()
        username_entry = tk.Entry(self.main_frame, width=30)
        username_entry.pack(pady=10)

        def send_request():
            recipient_username = username_entry.get()
            recipient = None
            for user in self.users:
                if user.username == recipient_username:
                    recipient = user
                    break

            if recipient:
                if recipient.username == self.current_user.username:
                    tk.messagebox.showerror("Error", "You cannot send a friend request to yourself!")
                elif recipient_username in self.current_user.friends:
                    tk.messagebox.showerror("Error", "This user is already your friend!")
                elif recipient_username in self.current_user.friend_requests:
                    tk.messagebox.showerror("Error", "Friend request already sent!")
                else:
                    recipient.add_friend_request(self.current_user.username)
                    self.save_data("users.pkl", self.users)
                    tk.messagebox.showinfo("Success", f"Friend request sent to {recipient_username}!")
                    self.dashboard()
            else:
                tk.messagebox.showerror("Error", "User not found!")

        tk.Button(
            self.main_frame,
            text="Send Request",
            command=send_request,
            bg="#2E86C1",
            fg="white",
            width=15,
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=20)

    def accept_friend_request(self, sender):
        if sender not in self.current_user.friends:
            self.current_user.friends.append(sender)
        if sender in self.current_user.friend_requests:
            self.current_user.friend_requests.remove(sender)
        for user in self.users:
            if user.username == sender:
                if self.current_user.username not in user.friends:
                    user.friends.append(self.current_user.username)
                break
        self.save_data("users.pkl", self.users)
        tk.messagebox.showinfo("Success", f"You are now friends with {sender}!")
        self.friend_requests_screen()

    def reject_friend_request(self, sender):
        if sender in self.current_user.friend_requests:
            self.current_user.friend_requests.remove(sender)
        self.save_data("users.pkl", self.users)
        tk.messagebox.showinfo("Info", f"Friend request from {sender} rejected!")
        self.friend_requests_screen()

    def notifications_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Notifications",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)

        if not self.current_user.notifications:
            tk.Label(self.main_frame, text="No notifications.", bg="#F0F8FF").pack()
        else:
            for notification in self.current_user.notifications:
                tk.Label(
                    self.main_frame,
                    text=notification,
                    bg="#F0F8FF",
                    anchor="w",
                    wraplength=500,
                ).pack(pady=5, padx=10)

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=20)

    def friend_list_screen(self):
        self.clear_frame()
        tk.Label(
            self.main_frame,
            text="Friend List",
            font=("Arial", 18, "bold"),
            bg="#2980B9",
            fg="white",
        ).pack(pady=20)


        if not self.current_user.friends:
            tk.Label(self.main_frame, text="No friends yet.", bg="#F0F8FF").pack()
        else:
            for friend in self.current_user.friends:
                friend_frame = tk.Frame(self.main_frame, bg="#F0F8FF", bd=1, relief="solid")
                friend_frame.pack(pady=5, padx=10, fill="x")
                tk.Label(friend_frame, text=f"Friend: {friend}", bg="#F0F8FF").pack(pady=2, padx=5)

                tk.Button(
                    friend_frame,
                    text="Remove Friend",
                    command=lambda f=friend: self.remove_friend(f),
                    bg="#E74C3C",
                    fg="white",
                    width=15,
                ).pack(side="right", padx=5)

                tk.Button()

        tk.Button(
            self.main_frame,
            text="Back",
            command=self.dashboard,
            bg="#AED6F1",
            fg="#2C3E50",
            width=15,
        ).pack(pady=20)

    def remove_friend(self, friend):
        self.current_user.friends.remove(friend)
        for user in self.users:
            if user.username == friend:
                user.friends.remove(self.current_user.username)
                break
        self.save_data("users.pkl", self.users)
        tk.messagebox.showinfo("Success", f"{friend} removed from your friend list!")
        self.friend_list_screen()

    def logout(self):
        self.current_user = None
        self.setup_gui()
 

if __name__ == "__main__":
    root=tk.Tk() 
    app=SocialMediaApp(root) 
    root.mainloop()
 