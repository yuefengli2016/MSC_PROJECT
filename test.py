import sys
import numpy as np
stdout = sys.stdout
from hyperstream import HyperStream, TimeInterval, UTC, Tool, StreamInstance
from datetime import datetime, timedelta
sys.stdout = stdout

hs = HyperStream()
print(hs)

averageperceptron = hs.plugins.online_learning.tools.averageperceptron()
#ogdtypeone = hs.plugins.online_learning.tools.ogdtypeone()
#passiveaggressiveone = hs.plugins.online_learning.tools.passiveaggressiveone()
#passiveaggressivetwo = hs.plugins.online_learning.tools.passiveaggressivetwo()
#passiveaggressivethree = hs.plugins.online_learning.tools.passiveaggressivethree()
#perceptron = hs.plugins.online_learning.tools.perceptron()
reader_tool = hs.plugins.online_learning.tools.csv_reader('plugins/online_learning/data/wdbc_data.csv')
#clock = hs.tools.clock()
#rng = hs.plugins.data_generators.tools.random(seed=1234)

wdbc_data_stream = hs.channel_manager.memory.get_or_create_stream("wdbc_data")
output = hs.channel_manager.memory.get_or_create_stream("output")

ti = TimeInterval(datetime(1960, 1, 1).replace(tzinfo=UTC), datetime(2007, 5, 1).replace(tzinfo=UTC))
reader_tool.execute(sources=[], sink=wdbc_data_stream, interval=ti)
wdbc_data_stream.calculated_intervals

ti = TimeInterval(datetime(1960, 1, 1).replace(tzinfo=UTC), datetime(2007, 5, 1).replace(tzinfo=UTC))
for key, value in wdbc_data_stream.window(ti).items():
    print '[%s]: %s' % (key,value)

averageperceptron.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
#perceptron.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
#passiveaggressiveone.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
#passiveaggressivetwo.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
#passiveaggressivethree.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
#ogdtypeone.execute(sources=[wdbc_data_stream], sink=output, interval=ti)
for key, value in output.window().items():
    print '[%s]: %s' % (key, value)
