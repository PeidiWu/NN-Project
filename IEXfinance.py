from iexfinance import get_market_book, get_market_deep, get_historical_data
from datetime import datetime
import matplotlib.pyplot as plt
import json
import sched, time
import csv

# start = datetime(2018, 3, 15)
# end = datetime(2018, 4, 24)

# df = get_historical_data("AAPL", start, end, 'json')
# datetime.strftime(df['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')


df = get_market_deep("amzn,googl,goog,msft,fb,intc,csco,nvda,nflx,jpm", 'json')
# json_f = open('/NN/Historical Data/IEX/AAPL_DEEP_Test.json')
# df = json.load(json_f)

csv_f = csv.writer(open("test_other_stocks.csv", 'w', newline=''))

header = df.keys()
csv_f.writerow(header)
csv_f.writerow(df.values())

# starttime = time.time()
# while True:
#   df = get_market_deep("amzn,googl,goog,msft,fb,intc,csco,nvda,nflx", 'json')
#   csv_f.writerow(df.values())
#   print("Recorded at: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#   time.sleep(5.0 - ((time.time() - starttime) % 5.0))


# print(json.dumps(df, indent=4, sort_keys=True))
# print(df['bids'])
# print(df['asks'])

# with open('AAPL_DEEP_Test.json','w') as fd:
#         json.dump(df, fd)

# s = sched.scheduler(time.time, time.sleep)

# def write_to_json(): 
#     with open('AAPL_DEEP_Test.json','w') as fd:
#         json.dump(df, fd)
#     print('Written to file at %s' % datetime.now())

# s.enter(10, 1, write_to_json)
# s.run()

