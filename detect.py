import cv2
import pandas as pd
import argparse
import os

def draw_rectangles_with_labels(video_path, csv_path):
    # Load video
    cap = cv2.VideoCapture(video_path)

    # Get video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Load data from CSV file
    df = pd.read_csv(csv_path)

    # Create output folder if it doesn't exist
    os.makedirs("mp4/detect", exist_ok=True)

    # Create video writer object
    output_path = "mp4/detect/output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

    # Process each frame and draw rectangles with labels
    while cap.isOpened():
        ret, frame = cap.read()

        # Check if end of video is reached
        if not ret:
            break

        # Get current frame number
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

        # Get coordinates for current frame from CSV file
        frame_data = df[df['frame'] == int(current_frame)]

        # Draw rectangles on the current frame
        for _, row in frame_data.iterrows():
            x0, y0, x1, y1 = row['x0'], row['y0'], row['x1'], row['y1']
            abs_x0 = int(x0 * width)
            abs_y0 = int(y0 * height)
            abs_x1 = int(x1 * width)
            abs_y1 = int(y1 * height)

            cv2.rectangle(frame, (abs_x0, abs_y0), (abs_x1, abs_y1), (0, 255, 0), 2)

            id_value = str(row['frame'])
            cv2.putText(frame, id_value, (abs_x0, abs_y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display current frame with rectangles and labels
        cv2.imshow('Video', frame)

        # Save the frame to the output video
        output_video.write(frame)

        # Check for 'q' key press to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close windows
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser(description='Draw rectangles with labels on a video based on CSV coordinates.')
    parser.add_argument('--video', type=str, help='Path to the video file.')
    parser.add_argument('--csv', type=str, help='Path to the CSV file.')

    # Get command-line arguments
    args = parser.parse_args()

    # Check if video and CSV paths are provided
    if args.video and args.csv:
        # Call the function with video and CSV arguments
        draw_rectangles_with_labels(args.video, args.csv)
    else:
        print('Please provide the video and CSV file paths.')
