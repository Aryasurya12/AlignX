"""Timing and memory instrumentation utilities for the AlignX pipeline."""

import time
import tracemalloc
from typing import Dict, Any, Callable, Tuple
from contextlib import contextmanager


class StageTimer:
    """Context manager for measuring stage runtimes in seconds."""

    def __init__(self, stage_name: str, store: Dict[str, float]):
        self.stage_name = stage_name
        self.store = store
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start_time
        self.store[self.stage_name] = elapsed


@contextmanager
def track_pipeline_resources() -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Context manager that tracks memory and returns (timings, memory_stats).
    """
    timings: Dict[str, float] = {}
    memory_stats: Dict[str, float] = {"current_kb": 0.0, "peak_kb": 0.0}

    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start()
        tracemalloc.reset_peak()

    t_start = time.perf_counter()
    try:
        yield timings, memory_stats
    finally:
        t_total = time.perf_counter() - t_start
        timings["total"] = t_total

        current, peak = tracemalloc.get_traced_memory()
        memory_stats["current_kb"] = round(current / 1024.0, 2)
        memory_stats["peak_kb"] = round(peak / 1024.0, 2)

        if not was_tracing:
            tracemalloc.stop()


def timed(stage_name: str):
    """Decorator to time standalone functions into an optional timings dictionary."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - t0
            # If kwargs contains a timings dict, store elapsed
            if "timings" in kwargs and isinstance(kwargs["timings"], dict):
                kwargs["timings"][stage_name] = elapsed
            return result
        return wrapper
    return decorator
