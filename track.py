import numpy as np
import cv2

frame = None
roiPts = []
inputMode = False
roiHist = None
roiBox = None

def selectROI(event, x, y, flags, param):
    global frame, roiPts, inputMode
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

def main():
    global frame, roiPts, inputMode, roiHist, roiBox

    camera = cv2.VideoCapture(0)

    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)

    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    roiBox = None

    while True:
        (grabbed, frame) = camera.read()
        if not grabbed:
            break

        if roiBox is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            backProj = cv2.calcBackProject([hsv], [0, 1], roiHist, [0, 180, 0, 256], 1)
            (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
            pts = cv2.boxPoints(r).astype(int)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            x, y, w, h = roiBox
            frame_h, frame_w = frame.shape[:2]
            if w * h > 0.5 * frame_w * frame_h:
                roiBox = None
                cv2.putText(frame, "Object lost. Press 'i' to reselect.",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("i") and len(roiPts) < 4:
            inputMode = True
            orig = frame.copy()
            roiPts.clear()
            while len(roiPts) < 4:
                cv2.imshow("frame", frame)
                cv2.waitKey(0)

            inputMode = False
            roiPtsNP = np.array(roiPts)
            s = roiPtsNP.sum(axis=1)
            tl = roiPtsNP[np.argmin(s)]
            br = roiPtsNP[np.argmax(s)]

            roi = orig[tl[1]:br[1], tl[0]:br[0]]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            roiHist = cv2.calcHist([roi], [0, 1], None, [16, 16], [0, 180, 0, 256])
            roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
            roiBox = (tl[0], tl[1], br[0] - tl[0], br[1] - tl[1])

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
