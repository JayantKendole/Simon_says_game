import pyttsx3

def speak_text(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Optional: Adjust the speech properties like rate and volume
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Speak the provided text
    engine.say(text)
    engine.runAndWait()

# Example usage
if __name__ == "__main__":
    instruction = "Simon says show thumbs up."
    speak_text(instruction)
