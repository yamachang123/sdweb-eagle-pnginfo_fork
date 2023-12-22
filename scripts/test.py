import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from datetime import datetime, timedelta

from test3 import Test3  # test3.py の中の Test3 クラスをインポート


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".png"):
            print(f"New PNG file detected: {event.src_path}")
            # ここでeagle-pnginfo.pyを実行
            # subprocess.run(["python", "C:\\GitHub\\sdweb-eagle-pnginfo_fork\\scripts\\eagle-pnginfo.py", event.src_path])
            
            testClass3=Test3('aaaaaa')
            testClass3.testMes()
            
            print(event.src_path, datetime.now())
            
            
            
def watch_folder(folder_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_watch = r"O:\wk"
    watch_folder(folder_to_watch)