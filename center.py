import cv2
import argparse
import os

def process_video(video_path):
    # Create the "mp4/center" directory if it doesn't exist
    os.makedirs("mp4/center", exist_ok=True)

    # Load the video
    cap = cv2.VideoCapture(video_path)

    # Get the video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = "mp4/center/output.mp4"
    output_video = cv2.VideoWriter(output_path, fourcc, 30, (416, 416))

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if the end of the video is reached
        if not ret:
            break

        # Extract the central object
        center_x = width // 2
        center_y = height // 2
        object_size = 416
        x0 = center_x - object_size // 2
        y0 = center_y - object_size // 2
        x1 = center_x + object_size // 2
        y1 = center_y + object_size // 2

        # Crop the frame based on the coordinates of the central object
        cropped_frame = frame[y0:y1, x0:x1]

        # Resize the cropped frame to 416x416
        resized_frame = cv2.resize(cropped_frame, (416, 416))

        # Display the current frame
        cv2.imshow('Video', resized_frame)

        # Save the current frame to the output video
        output_video.write(resized_frame)

        # Check if the 'q' key is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close windows
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process video and save the center object.')
    parser.add_argument('--video', type=str, help='Path to the video file.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the video path argument is provided
    if args.video:
        # Call the video processing function with the video path argument
        process_video(args.video)
    else:
        print('Please provide the path to the video file.')
