import sys
import os
import json

from datetime import datetime
from datetime import timedelta
from collections import Counter
import time
import pickle
from analyser import Analyser
from call_analyser import CallAnalyser
from message_analyser import MessageAnalyser

if __name__ == "__main__":
  history_directory = sys.argv[1]
  analyser = Analyser(history_directory)

  call_analyser = CallAnalyser(analyser)
  call_stats = call_analyser.get_call_stats()
  message_analyser = MessageAnalyser(analyser)
  message_stats = message_analyser.get_message_stats()
  
  stats = {
    'call_stats': call_stats,
    'message_stats': message_stats,
  }
  print("Storing stats as json")
  with open('data.json', 'w') as fp:
    json.dump(stats, fp)