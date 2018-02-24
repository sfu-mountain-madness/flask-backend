import asyncio
import functools
import threading
from concurrent.futures import ThreadPoolExecutor


class SyncToAsync:
  thread_pool = ThreadPoolExecutor()
  thread_local = threading.local()
  
  def __init__(self, func):
    self.func = func
  
  async def __call__(self, *args, **kwargs):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(self.thread_pool,
                                  functools.partial(self.thread_handler, loop, *args, **kwargs))
    return await asyncio.wait_for(future, timeout=None)
  
  def __get__(self, instance, owner):
    return functools.partial(self.__call__, instance)
  
  def thread_handler(self, loop, *args, **kwargs):
    self.thread_local.main_event_loop = loop
    return self.func(*args, **kwargs)


sync_to_async = SyncToAsync
