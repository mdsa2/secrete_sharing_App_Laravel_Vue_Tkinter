import random
import string
from tkinter import *
import time

from api_handler import ApiHandler


class SecretSharingApp:
    def __init__(self, master):
        self.master = master
        master.title("Secret Sharing Tool")

        # Initialize variables
        self.secret_entry = Entry(master)
        self.num_shares_entry = Entry(master)
        self.shares_text = Text(master, height=10, width=30)
        self.reconstructed_text = Text(master, height=1, width=30)
        self.result_text = StringVar()

        # Initialize share generation time
        self.share_generation_time = None

        # Timer for periodic share check
        self.master.after(1000, self.check_share_expiry)

        # Create labels and buttons
        secret_label = Label(master, text="Secret:")
        secret_label.pack()
        self.secret_entry.pack()

        num_shares_label = Label(master, text="Number of Shares ( 4):")
        num_shares_label.pack()
        self.num_shares_entry.pack()

        generate_button = Button(master, text="Generate Shares", command=self.generate_shares_gui)
        generate_button.pack()

        reconstruct_button = Button(master, text="Reconstruct Secret", command=self.reconstruct_secret_gui)
        reconstruct_button.pack()

        shares_label = Label(master, text="Shares:")
        shares_label.pack()
        self.shares_text.pack()

        reconstructed_label = Label(master, text="Reconstructed Secret:")
        reconstructed_label.pack()
        self.reconstructed_text.pack()

        result_label = Label(master, textvariable=self.result_text)
        result_label.pack()

        # Initialize ApiHandler
        self.api_handler = ApiHandler()

    def create_table(self):
        # This is handled by Laravel migrations, so no need for a local table creation
        pass

    def save_shares(self, shares):
        # Instead of saving locally, send shares to Laravel API
        response = self.api_handler.send_shares(shares)

        if response.status_code == 200:
            self.result_text.set("Shares generated and saved in database.")
            self.share_generation_time = time.time()  # Record share generation time
        else:
            self.result_text.set("Failed to send data to Laravel.")

    def generate_random_secret(self):
        # Generate a random string as the secret
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def generate_shares_gui(self):
        num_shares = int(self.num_shares_entry.get())

        if num_shares < 4 or num_shares > 4:
            self.result_text.set("Invalid number of shares.")
            return

        # Create the shares table
        self.create_table()

        # Generate shares
        shares = []
        secret = self.generate_random_secret()
        for i in range(1, num_shares + 1):
            x = i
            y = random.randint(100000000, 999999999)  # Generate a random number for y
            shares.append({'x': x, 'y': y})

        # Save shares to the database
        self.save_shares(shares)

        # Display shares
        self.shares_text.delete(3.0, END)
        for share in shares:
            self.shares_text.insert(END, f"Share: {share['x']}, {share['y']}\n")

        self.result_text.set("Shares generated and saved in GUI.")

    def reconstruct_secret_gui(self):
        # Retrieve shares from the GUI (shares generated locally)
        shares = []
        shares_text = self.shares_text.get("1.0", END).strip().split("\n")
        for share_text in shares_text:
            if share_text.startswith("Share: "):
                share_text = share_text[len("Share: "):]  # Remove the "Share: " prefix
                x, y = map(int, share_text.split(", "))
                shares.append({'x': x, 'y': y})

        if not shares:
            self.result_text.set("No shares available for reconstruction.")
            return

        # Reconstruct the secret using the received shares
        try:
            reconstructed_secret = self.reconstruct_secret(shares)
            self.result_text.set(f"Reconstructed Secret: {reconstructed_secret}")
            self.reconstructed_text.delete(1.0, END)
            self.reconstructed_text.insert(END, reconstructed_secret)
        except ValueError as e:
            self.result_text.set(str(e))
            self.reconstructed_text.delete(1.0, END)

    def reconstruct_secret(self, shares):
        secret_sum = 0
        for share in shares:
            secret_sum += share['y']
        reconstructed_secret = str(secret_sum)
        return reconstructed_secret
    def check_share_expiry(self):
        if self.share_generation_time is not None:
            current_time = time.time()
            time_difference = current_time - self.share_generation_time
            if time_difference >= 120:  # 5 minutes (300 seconds)
                # Delete shares from GUI
                self.shares_text.delete(1.0, END)
                self.reconstructed_text.delete(1.0, END)
                self.result_text.set("Shares expired and deleted.")

                # Delete shares from database
                self.api_handler.delete_shares()  # Implement this method in ApiHandler

                # Reset share generation time
                self.share_generation_time = None

        # Schedule the next check after 1 second
        self.master.after(1000, self.check_share_expiry)




if __name__ == "__main__":
    root = Tk()
    app = SecretSharingApp(root)
    root.mainloop()