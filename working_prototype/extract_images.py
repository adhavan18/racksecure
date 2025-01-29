import cv2
import os

# Path to your video
video_path = r"c:\Users\saduv\Videos\Camera_13_UB_ENTRANCE_UB_ENTRANCE_20250127155000_20250127160558_198544198.mp4"

# Output folder for extracted frames
output_folder = "extracted_frames"
os.makedirs(output_folder, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Frame count
frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break  # End of video

    # Save every nth frame (e.g., every 10th frame)
    if frame_count % 10 == 0:  # Adjust '10' to control the frequency
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)

    frame_count += 1

cap.release()
print(f"Frames saved in {output_folder}")