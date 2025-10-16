from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

THREADPOOL: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=int(cpu_count() or 32))
