import tkinter as tk 
from tkinter import messagebox 
from PIL import Image, ImageTk
import pickle 
class User: 
    def __init__(self, username, password, age):
        self.username = username
        self.password = password
        self.age = age
        self.liked_posts = set()  

    def display_info(self):
        return f"User: {self.username}, Age: {self.age}"

class Post:
    def __init__(self, content, author, tags):
        self.content = content
        self.author = author
        self.tags = tags
        self.comments=list() 
        self.likes=0   
        self.liked_by=set()   

    def add_comment(self, comment):
        self.comments.append(comment)

class BuddyBoard: 
    def __init__(self, root):
        self.root = root
        self.root.title("BuddyBoard")
        self.root.geometry("800x600")
        self.main_frame = tk.Frame(self.root, bg="#F0F8FF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.logo_image = Image.open(r"C:/Users/PC/Downloads/BuddyBoard.jpeg")
        self.logo_image = self.logo_image.resize((50, 50), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)       
        self.users=[] 
        self.posts=[] 
        self.users=self.load_data("users.pkl",list())
        self.posts=self.load_data("posts.pkl",list())  
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
        tk.Label(self.main_frame,text="Welcome to BuddyBoard",font=("Arial", 24, "bold"),bg="#2980B9",fg="white",).pack(fill=tk.X, pady=20)
        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)
        tk.Button(self.main_frame,text="Hop Back In!",command=self.login_screen,font=("Arial", 14),bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)
        tk.Button(self.main_frame,text="Join the Club",command=self.register_screen,font=("Arial", 14),bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)

    def login_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame,text="Hop Back In!",font=("Arial", 18, "bold"),bg="#2980B9",fg="white",).pack(pady=20)
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
            if not username or not password:
                messagebox.showerror('Error','Please Enter Complete Login Details!') 
                return 
            for user in self.users:
                if user.username == username and user.password == password:
                    self.current_user = user
                    messagebox.showinfo("Success",f"{user.username} Logged In!")
                    self.Homepage()

                    return
            messagebox.showerror("Error","Invalid username or password!")

        tk.Button(self.main_frame,text="Hop Back In!",command=login,bg="#2E86C1",fg="white",width=15,).pack(pady=20)
        tk.Button(self.main_frame,text="Return",command=self.setup_gui,bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)

    def register_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame,text="Join the Club",font=("Arial", 18, "bold"),bg="#2980B9",fg="white",).pack(pady=20)
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
            if not username or not password or not age:
                messagebox.showerror('Error','Please Enter Complete Registration Details!')
                return 
 
            elif not username or not password or not age.isdigit():
                messagebox.showerror('Error',"Invalid input!")
                return
            elif int(age)<12 or int(age)>75: 
                messagebox.showerror('Error','Your Entered Age is Either Below Age Limit (less than 12) or too high')
                return 

            for user in self.users:
                if user.username == username:
                    messagebox.showerror("USER ERROR","UAV-20\nUsername already exists!")
                    return

            new_user = User(username, password, age)

            self.users.append(new_user)
            self.save_data("users.pkl", self.users)
            messagebox.showinfo("Success","Registration successful!")
            self.login_screen()
        tk.Button(self.main_frame,text="Join the Club",command=register,bg="#2E86C1",fg="white",width=15,).pack(pady=20)
        tk.Button(self.main_frame,text="Return",command=self.setup_gui,bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)
    def Homepage(self):
        self.clear_frame()
        tk.Label(self.main_frame,text=f"Welcome, {self.current_user.username}",font=("Arial", 18, "bold"),bg="#2980B9",fg="white",).pack(pady=20)
        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)
        tk.Button(self.main_frame,text="Post Something",command=self.new_post_screen,bg="#AED6F1",fg="#2C3E50",width=20,).pack(pady=10)
        tk.Button(self.main_frame,text="View Posts",command=self.view_posts_screen,bg="#AED6F1",fg="#2C3E50",width=20,).pack(pady=10)
        tk.Button(self.main_frame,text="Logout",command=self.logout,bg="#AED6F1",fg="#2C3E50",width=20).pack(pady=10)
    def new_post_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame,text="Share your thoughts",font=("Helvetica", 18, "bold"),bg="#2E8B57",fg="white",).pack(pady=20)
        tk.Label(self.main_frame, image=self.logo_photo, bg="#2980B9").pack(pady=10)
        tk.Label(self.main_frame, text="What's on your mind?", bg="#F0F8FF").pack()
        content_entry = tk.Entry(self.main_frame, width=50)
        content_entry.pack(pady=10)
        tk.Label(self.main_frame, text="Add some tags #:", bg="#F0F8FF").pack()
        tagsentry = tk.Entry(self.main_frame, width=50)
        tagsentry.pack(pady=10)

        def new_post():
            content = content_entry.get()
            tags = tagsentry.get().split(',') 
            if content:
                new_post = Post(content, self.current_user.username, tags)
                self.posts.append(new_post)
                self.save_data("posts.pkl", self.posts)
                self.save_data("users.pkl", self.users)
                messagebox.showinfo("Congratulations", "Your ideas are shared")
                self.Homepage()
            else:
                messagebox.showerror("Error", "Error Code: eur09A\nPost content cannot be empty!")

        tk.Button(self.main_frame,text="Post Something!",command=new_post,bg="#2E86C1",fg="white",width=20,).pack(pady=20)
        tk.Button(self.main_frame,text="Return",command=self.Homepage,bg="#AED6F1",fg="#2C3E50",width=15,).pack(pady=10)

    def view_posts_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame,text="Activity",font=("Arial", 18, "bold"),bg="#2980B9",fg="white",).pack(pady=20)

        canvas = tk.Canvas(self.main_frame, bg="#F0F8FF")
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F0F8FF")
        scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))   
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.posts:
            tk.Label(scrollable_frame, text="You have no Posts, Start sharing your ideas to the world", bg="#F0F8FF").pack()
        else:
            for post in reversed(self.posts): 
                post_frame = tk.Frame(scrollable_frame, bg="#FFFFFF",bd=1, relief="solid")
                post_frame.pack(pady=5, padx=10, fill="x")
                tk.Label(post_frame, text=f"Author: {post.author}", bg="#FFFFFF", font=("Arial", 12, "bold")).pack(pady=2, padx=5)
                tk.Label(post_frame, text=f"Tags: {', '.join(post.tags)}", bg="#FFFFFF", font=("Arial", 10)).pack(pady=2, padx=5)
                tk.Label(post_frame, text=post.content, bg="#FFFFFF", font=("Arial", 12), wraplength=500).pack(pady=2, padx=5)
                tk.Label(post_frame, text=f"Likes: {post.likes}", bg="#FFFFFF", font=("Arial", 10)).pack(pady=2, padx=5)

                def like_post(post=post):  
                    if post in self.current_user.liked_posts:
                        messagebox.showerror("Error", "You have already liked this post!")
                        return
                    post.likes+=1
                    post.liked_by.add(self.current_user.username)
                    self.current_user.liked_posts.add(post)
                    self.save_data("posts.pkl", self.posts)
                    messagebox.showinfo("Success", "You liked the post!")
                    self.view_posts_screen()

                tk.Button(post_frame,text="Like",command=like_post,bg="#2ECC71",fg="white",font=("Arial", 10),width=10,).pack(side="left", padx=5)

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
                            messagebox.showinfo("Success", "Comment added!")
                            comment_window.destroy()
                            self.view_posts_screen()
                        else:
                            messagebox.showerror("Error", "Comment cannot be empty!")
                    tk.Button(comment_window, text="Submit", command=submit_comment, bg="#3498DB", fg="white", font=("Arial", 10)).pack(pady=5)

                tk.Button(post_frame,text="Comment",command=add_comment,bg="#3498DB",fg="white",font=("Arial", 10),width=10,).pack(side="left", padx=5)

                for comment in post.comments:
                    tk.Label(post_frame, text=comment, bg="#FFFFFF", font=("Arial", 10), wraplength=500, anchor="w").pack(pady=2, padx=5)

                if post.author == self.current_user.username:
                    tk.Button(post_frame,text="Delete Post",command=lambda p=post: self.delete_post(p),bg="#FF6347",fg="white",font=("Arial", 10),width=10,).pack(side="right", padx=5)

        tk.Button(self.main_frame,text="Return",command=self.Homepage,bg="#AED6F1",
            fg="#2C3E50",width=15,).pack(pady=20)

    def delete_post(self, post):
        self.posts.remove(post)
        self.save_data("posts.pkl", self.posts)
        messagebox.showinfo("Success", "Post deleted successfully!")
        self.view_posts_screen()


    def logout(self):
        self.current_user=None 
        self.setup_gui()


if __name__ == "__main__":
    root=tk.Tk() 
    app=BuddyBoard(root) 
    root.mainloop()
 