import cv2
from splash_screen import show_splash_screen
import game_logic
import speaker

def main():
    # Show the splash screen first
    show_splash_screen()

    # Initialize the camera
    cap = cv2.VideoCapture(0)  # Use the first connected camera

    # Check if the camera is opened correctly
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    # Define the speaker callback
    def speaker_callback(text):
        speaker.speak_text(text)  # Pass the text to the speak_text function

    # Start the game logic
    try:
        game_logic.start_game_logic(cap, speaker_callback)
    except Exception as e:
        print(f"Error occurred during the game: {e}")
    finally:
        # Release the camera resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
