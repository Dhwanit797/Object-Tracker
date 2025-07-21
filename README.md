# Object Tracker using Python and OpenCV (CamShift)

This project implements a real-time object tracking system using Python and OpenCV's CamShift algorithm. The tracker uses color histogram backprojection to follow a user-selected object in a video stream captured from the webcam.

### Features
- Real-time tracking of user-selected objects.
- Interactive ROI (Region of Interest) selection using mouse clicks.
- Dynamic tracking window that adjusts to object movement, size, and rotation.
- Robust handling when the object leaves the frame, with prompts to reselect.
- Utilizes both Hue and Saturation channels in HSV color space for improved accuracy.

### How to Use
Run the script, press `i` to select an object by clicking four points around it, and watch it be tracked live. If tracking is lost, you can reinitialize it by pressing `i` and selecting again. Press `q` to quit.

### Technologies Used
- Python
- OpenCV
- NumPy

### Note on Development
This project was developed with the assistance of AI tools to accelerate coding and debugging. While AI helped with structuring and refining the code, the implementation and customization were guided based on standard computer vision principles and user needs.
