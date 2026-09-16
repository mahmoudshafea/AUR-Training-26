import cv2

class task2:
    def __init__(self,video_path="thrown_shapes_noisy_30s.mp4"):
        self.cap=cv2.VideoCapture(video_path)
        self.detect_shapes()


    def detect_shapes(self):
        while True:
            ret,frame=self.cap.read()
            if not ret:
                print("Cannot receive frame")
                break
            blurred=cv2.GaussianBlur(frame,(5,5),0)
            hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
            lower_red = (0, 100, 100)
            upper_red = (10, 255, 255)

            red_mask = cv2.inRange(hsv,lower_red,upper_red)

            lower_blue = (90, 100, 100)
            upper_blue = (130, 255, 255)

            blue_mask = cv2.inRange(hsv,lower_blue,upper_blue)

            red_contours, _ = cv2.findContours(red_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            blue_contours, _ = cv2.findContours(blue_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


            for contour in red_contours:

                area = cv2.contourArea(contour)

                if area < 500:
                    continue

                perimeter = cv2.arcLength(contour,True)

                if perimeter == 0:
                    continue

                circularity = (4 * 3.14159 * area/ (perimeter * perimeter))
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                if circularity > 0.4 and len(approx) > 6:
                    cv2.drawContours(frame,[contour],-1,(0, 0, 0),2)

            for contour in blue_contours:

                area = cv2.contourArea(contour)

                if area < 500:
                    continue

                perimeter = cv2.arcLength(contour,True)

                if perimeter == 0:
                    continue

                approx = cv2.approxPolyDP(contour,0.04 * perimeter,True)

                if len(approx) == 4:
                    cv2.drawContours(frame,[contour],-1,(0, 0, 0),2)

            cv2.imshow("Shape Detection", frame)

            if cv2.waitKey(30) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


detector = task2()
            




