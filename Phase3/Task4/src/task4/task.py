import cv2
from ultralytics import YOLO


DISTANCE_M = 9.144

LINE_A = (70, 90, 230, 90)
LINE_B = (15, 125, 225, 125)

CONF = 0.3


class SpeedLine:
    def __init__(self, x1, y, x2):
        self.x1 = x1
        self.y = y
        self.x2 = x2

    def crossed(self, previous_y, current_y):
        if previous_y is None:
            return False

        return (
            previous_y < self.y and current_y >= self.y
        ) or (
            previous_y > self.y and current_y <= self.y
        )

    def draw(self, frame):
        cv2.line(
            frame,
            (self.x1, self.y),
            (self.x2, self.y),
            (0, 255, 255),
            2
        )


class Vehicle:
    def __init__(self, track_id):
        self.track_id = track_id
        self.previous_y = None
        self.cross_a = None
        self.cross_b = None
        self.speed = None

    def update(self, current_y, current_time, line_a, line_b):
        if self.cross_a is None:
            if line_a.crossed(self.previous_y, current_y):
                self.cross_a = current_time

        elif self.cross_b is None:
            if line_b.crossed(self.previous_y, current_y):
                self.cross_b = current_time

                elapsed_time = self.cross_b - self.cross_a

                if elapsed_time > 0:
                    self.speed = (
                        DISTANCE_M / elapsed_time
                    ) * 3.6

        self.previous_y = current_y


class SpeedDetector:
    def __init__(self, model_path, video_path):
        self.model = YOLO(model_path)
        self.video_path = video_path

        self.line_a = SpeedLine(
            LINE_A[0],
            LINE_A[1],
            LINE_A[2]
        )

        self.line_b = SpeedLine(
            LINE_B[0],
            LINE_B[1],
            LINE_B[2]
        )

        self.vehicles = {}

    def process(self):
        cap = cv2.VideoCapture(self.video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)

        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                break

            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
            current_time = frame_number / fps

            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=CONF
            )

            boxes = results[0].boxes

            if boxes.id is not None:

                for (
                    box,
                    track_id
                ) in zip(
                    boxes.xyxy.int().tolist(),
                    boxes.id.int().tolist()
                ):

                    x1, y1, x2, y2 = box

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if track_id not in self.vehicles:
                        self.vehicles[track_id] = Vehicle(track_id)

                    vehicle = self.vehicles[track_id]

                    vehicle.update(
                        cy,
                        current_time,
                        self.line_a,
                        self.line_b
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        frame,
                        (cx, cy),
                        4,
                        (0, 0, 255),
                        -1
                    )

                    text = f"ID: {track_id}"

                    if vehicle.speed is not None:
                        text += f"  Speed: {vehicle.speed:.1f} km/h"

                    cv2.putText(
                        frame,
                        text,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

            self.line_a.draw(frame)
            self.line_b.draw(frame)

            cv2.putText(
                frame,
                "A",
                (self.line_a.x1, self.line_a.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "B",
                (self.line_b.x1, self.line_b.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.imshow("Radar Speed Detector", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


