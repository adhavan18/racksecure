import cv2
import numpy as np

# Load video
video_path = r"C:/Users/gmbas/OneDrive/Desktop/adhavan.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))

# Define output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output_with_rack_grid.avi", fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection to find shelves and racks
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours (shelves & racks)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Detected Contours: {len(contours)}")  # Debugging line

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Debugging: Draw all bounding boxes to check what is detected
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)  # Light blue rectangles

        # Aspect Ratio & Solidity Filtering (Adjust these)
        aspect_ratio = w / float(h)  # Width-to-height ratio
        solidity = cv2.contourArea(contour) / (w * h)  # How solid the shape is

        # Filtering criteria for racks
        if w > frame_width * 0.2 and h > frame_height * 0.1 and 0.3 < aspect_ratio < 2.5 and solidity > 0.3:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green for detected racks
            
            # Define Grid Inside Racks
            rows, cols = 4, 3  # Adjust based on your racks
            cell_width = w // cols
            cell_height = h // rows

            # Draw grid inside detected rack
            for i in range(1, cols):
                cv2.line(frame, (x + i * cell_width, y), (x + i * cell_width, y + h), (0, 255, 255), 2)  # Yellow grid

            for i in range(1, rows):
                cv2.line(frame, (x, y + i * cell_height), (x + w, y + i * cell_height), (0, 255, 255), 2)

    out.write(frame)

    # Show frame with detected racks and grid
    cv2.imshow('Rack Grid Debug', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()