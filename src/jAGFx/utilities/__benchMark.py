import time
from functools import wraps
from typing import List, Optional

from jAGFx.logger import debug


def Benchmark(checkpoints: List[int], filepath: Optional[str] = None):
    def decorator(func):
        stats = {
            "total_calls": 0,
            "total_time": 0.0,
            "longest_call": 0.0,
            "shortest_call": float("inf"),
        }

        sorted_checkpoints = sorted(list(set(checkpoints)))

        # A helper function to write formatted stats to a file
        def showStats(message):
            if filepath is not None:
                try:
                    with open(filepath, "a") as f:
                        f.write(message + "\n")

                except IOError as e:
                    debug(f"Error writing to file '{filepath}': {e}")
            else:
                debug(message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            stats["total_calls"] += 1
            stats["total_time"] += elapsed_time
            if elapsed_time > stats["longest_call"]:
                stats["longest_call"] = elapsed_time
            if elapsed_time < stats["shortest_call"]:
                stats["shortest_call"] = elapsed_time

            if stats["total_calls"] in sorted_checkpoints:
                message = (
                    f"\n--- Checkpoint Stats for '{func.__name__}' at {stats['total_calls']} calls ---\n"
                    f"Total time: {stats['total_time']:.6f}s\n"
                    f"Average time per call: {(stats['total_time'] / stats['total_calls']):.6f}s\n"
                    f"Longest call: {stats['longest_call']:.6f}s\n"
                    f"Shortest call: {stats['shortest_call']:.6f}s\n"
                    f"{'-' * 50}"
                )
                showStats(message)

            return result

        def print_final_stats():
            if stats["total_calls"] > 0:
                message = (
                    f"\n--- Final Benchmark Stats for '{func.__name__}' ---\n"
                    f"Total calls: {stats['total_calls']}\n"
                    f"Total time: {stats['total_time']:.6f}s\n"
                    f"Average time per call: {(stats['total_time'] / stats['total_calls']):.6f}s\n"
                    f"Longest call: {stats['longest_call']:.6f}s\n"
                    f"Shortest call: {stats['shortest_call']:.6f}s\n"
                    f"{'-' * 50}"
                )
                showStats(message)

        wrapper.print_final_stats = print_final_stats

        return wrapper

    return decorator
