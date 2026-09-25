import sys
import time
from pathlib import Path

# Add the app directory to Python's import path
APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from quality_checker import check_data_quality
from ai_analyzer import (
    analyze_quality_report,
    create_incident_report
)
from database import (
    initialize_database,
    save_quality_run
)


WATCH_FOLDER = APP_DIR.parent / "data" / "incoming"


class CSVHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".csv":
            return

        print("\n" + "=" * 60)
        print("NEW CSV FILE DETECTED")
        print("=" * 60)

        print(f"File: {file_path}")

        time.sleep(2)

        try:

            print("\nRunning data quality checks...")

            quality_report = check_data_quality(
                str(file_path)
            )

            initialize_database()

            save_quality_run(
                file_name=str(file_path),
                total_records=quality_report["total_records"],
                quality_score=quality_report["quality_score"],
                issue_count=len(quality_report["issues"]),
                created_at=time.strftime("%Y-%m-%dT%H:%M:%S")
            )

            print(
                f"Quality Score: "
                f"{quality_report['quality_score']}%"
            )

            print("\nSending report to Llama 3.2...")

            ai_analysis = analyze_quality_report(
                quality_report
            )

            print("\nAI ANALYSIS")
            print("-" * 60)
            print(ai_analysis)

            report_file = create_incident_report(
                quality_report,
                ai_analysis
            )

            print("\nINCIDENT REPORT CREATED")
            print("-" * 60)
            print(f"Report: {report_file}")

            print("\nProcessing completed successfully.")

        except Exception as error:

            print("\nERROR PROCESSING FILE")
            print("-" * 60)
            print(error)


def start_monitor():

    WATCH_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    event_handler = CSVHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        str(WATCH_FOLDER),
        recursive=False
    )

    observer.start()

    print("=" * 60)
    print("AI DATA QUALITY AUTOMATION")
    print("=" * 60)
    print(f"Monitoring folder: {WATCH_FOLDER}")
    print("Waiting for new CSV files...")
    print("Press CTRL+C to stop.")
    print("=" * 60)

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping monitor...")

        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_monitor()