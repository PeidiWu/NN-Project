import ijson
import datetime

with open('/NN/Historical Data/IEX/IEX HIST/IEX_DEEP_20170515.json') as f:
    data = ijson.items(f, '')


