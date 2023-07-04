import pstats
import cProfile

stats = pstats.Stats("background.stats")
stats.print_stats()


# profiler = cProfile.Profile()
# profiler.enable()

# profiler.disable()
# profiler.dump_stats("test.stats")