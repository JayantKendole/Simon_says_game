# game_logic.py
import random
import time
import cv2
import mediapipe as mp

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Instructions for the game
instructions = [
    "Simon says show 1 finger",
    "Simon says show 2 fingers",
    "Simon says show 3 fingers",
    "Simon says show 4 fingers",
    "Simon says show 5 fingers",
    "Simon says thumbs up",
    "Simon says thumbs down",
    "show 1 finger",
    "show 2 fingers",
    "show 3 fingers",
    "show 4 fingers",
    "show 5 fingers",
    "thumbs up",
    "thumbs down"
]

# Set the game state
score = 0
game_over = False

# Function to detect thumbs up or thumbs down
def check_thumbs_action(hand_landmarks):
    thumb_up = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
    thumb_down = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
    return thumb_up, thumb_down

# Function to count the number of fingers being held up
def check_fingers_action(hand_landmarks):
    # Check landmarks for index, middle, ring, pinky fingers
    fingers = [
        hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y
        for i in range(8, 21, 4)
    ]
    # Thumb is considered separately
    thumb_open = (
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
        > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    )
    return sum(fingers) + int(thumb_open)

# Function to run the game logic
def start_game_logic(cap, speaker_callback):
    global score, game_over

    # Wait 5 seconds before starting the game
    start_time = time.time()
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        cv2.imshow("Simon Says - Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    # Main game loop
    while not game_over:
        # Randomly choose an instruction
        random_action = random.choice(instructions)

        # Announce the instruction using the provided speaker callback
        speaker_callback(random_action)

        # Give the player 7 seconds to perform the action
        start_time = time.time()
        while time.time() - start_time < 7:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)

            # Process the frame for hand landmarks
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result_hands = hands.process(frame_rgb)

            # Initialize variables
            thumb_up, thumb_down = False, False
            finger_count = 0

            if result_hands.multi_hand_landmarks:
                for hand_landmarks in result_hands.multi_hand_landmarks:
                    thumb_up, thumb_down = check_thumbs_action(hand_landmarks)
                    finger_count = check_fingers_action(hand_landmarks)

            # Parse the finger count from the instruction if needed
            expected_fingers = None
            if "show" in random_action:
                # Extract the expected number of fingers
                try:
                    expected_fingers = int(random_action.split()[-2])
                except ValueError:
                    expected_fingers = None

            # Check if the correct action is performed
            if random_action.startswith("Simon says"):
                if "thumbs up" in random_action and thumb_up:
                    score += 1
                    break
                elif "thumbs down" in random_action and thumb_down:
                    score += 1
                    break
                elif "show" in random_action and expected_fingers is not None and finger_count == expected_fingers:
                    score += 1
                    break
            else:
                # If action is performed without "Simon says," game over
                if "thumbs up" in random_action and thumb_up:
                    game_over = True
                    break
                elif "thumbs down" in random_action and thumb_down:
                    game_over = True
                    break
                elif "show" in random_action and expected_fingers is not None and finger_count == expected_fingers:
                    game_over = True
                    break

            # Display the score and camera feed
            cv2.putText(frame, f"Score: {score}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Simon Says - Camera Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                game_over = True
                break

    cap.release()
    cv2.destroyAllWindows()
