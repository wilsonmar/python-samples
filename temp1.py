import time
print("Times")
print("%42.21f" % time.time())
print("%42.21f" % time.clock())
print("%42.21f" % time.monotonic())
print("%42.21f" % time.perf_counter())
print("%42.21f" % time.process_time())

print("Resolution in sec")
print("%.21f" % time.get_clock_info('time').resolution)
print("%.21f" % time.get_clock_info('clock').resolution)
print("%.21f" % time.get_clock_info('monotonic').resolution)
print("%.21f" % time.get_clock_info('perf_counter').resolution)
print("%.21f" % time.get_clock_info('process_time').resolution)