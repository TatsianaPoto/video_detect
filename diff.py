import cv2
import argparse
import os

def process_video(video_path):
    # Create the "img" directory if it doesn't exist
    os.makedirs("img", exist_ok=True)

    # Load the video
    cap = cv2.VideoCapture(video_path)

    # Initialize variables
    prev_frame = None
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if the end of the video is reached
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Skip frames that are similar to the previous frame
        if prev_frame is not None and cv2.norm(gray, prev_frame, cv2.NORM_L2) < 100:
            continue

        # Update the previous frame
        prev_frame = gray.copy()

        # Display the current frame
        cv2.imshow('Video', frame)

        # Save the current frame as an image
        frame_count += 1
        image_path = os.path.join("img", f"frame_{frame_count:05d}.png")
        cv2.imwrite(image_path, frame)

        # Check if the 'q' key is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process video and save distinct frames as images.')
    parser.add_argument('--video', type=str, help='Path to the video file.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the video path argument is provided
    if args.video:
        # Call the video processing function with the video path argument
        process_video(args.video)
    else:
        print('Please provide the path to the video file.')
