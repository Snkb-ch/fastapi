import time

def background_task(name: str, wait: int):
    print(f"Task {name} started! Waiting for {wait} seconds...")
    time.sleep(wait)
    print(f"Task {name} completed!")
