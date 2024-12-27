# splash_screen.py
import tkinter as tk

def on_continue_button_click(root):
    """
    Function to be executed when the continue button is clicked or Enter is pressed.
    It will close the splash screen window.
    """
    root.quit()  # Close the splash screen
    root.destroy()  # Destroy the splash screen window

def show_splash_screen():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Welcome to Simon Says")
    
    # Set the window size
    root.geometry("800x500")
    
    # Set the background color to a yellowish color
    root.config(bg='#FFFACD')  # Light yellow
    
    # Create and configure a label for the header
    header = tk.Label(root, text="Welcome to Simon Says", font=("Helvetica", 20, "bold"), fg="#FF7F50", bg="#FFFACD")
    header.pack(pady=20)  # Add padding
    
    # Define the instructions
    splash_text = """
    The objective is to follow the instructions that begin with "Simon says."
    If "Simon says" is not at the beginning of the instruction, do not perform the action.
    Every correct action earns the player +1 point.
    If the player performs the wrong action (without "Simon says"), they lose the game.
    The player must continue following the instructions to score points and avoid elimination.
    """
    
    # Create and configure a label for the instructions text
    instructions = tk.Label(root, text=splash_text, font=("Helvetica", 12), fg="black", bg="#FFFACD", wraplength=700)
    instructions.pack(pady=10)  # Add padding
    
    # Create and configure a "Continue" button
    continue_button = tk.Button(root, text="Continue", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=lambda: on_continue_button_click(root))
    continue_button.pack(pady=20)
    
    # Bind the "Enter" key to trigger the continue button action
    root.bind("<Return>", lambda event: on_continue_button_click(root))
    
    # Start the Tkinter main loop
    root.mainloop()
