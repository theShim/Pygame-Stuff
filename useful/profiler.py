import pstats
import cProfile

stats = pstats.Stats("test.stats")
stats.print_stats()


# profiler = cProfile.Profile()
# profiler.enable()

# profiler.disable()
# profiler.dump_stats("test.stats")