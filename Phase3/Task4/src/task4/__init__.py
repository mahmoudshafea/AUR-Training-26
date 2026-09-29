from .task import SpeedDetector
def main() -> None:  
    detector = SpeedDetector(
        "best.pt",
        "Task_Video.mp4"
    )

    detector.process()