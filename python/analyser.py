import sys
import os

from datetime import datetime
from datetime import timedelta
from objects import Message, Sender, Call
import time
import pickle

SMALLER_SIZE = False

class Analyser:
  messages = []
  senders = {}
  calls = []
  
  def __init__(self, history_directory, use_cache=True):
    cache_file = history_directory + '/cache.data'
    if use_cache:
        # Read parsed data from cache
        try:
            f = open(cache_file, "rb")
            t_start = time.clock()
            print("Parsing cached data...")
            self.messages, self.senders, self.calls = pickle.load(f)
            print("Parsed %d messages in %.4f seconds" % (self.total_count(), time.clock()-t_start))
            return
        except IOError:
            pass
        except pickle.PickleError:
            print("Error parsing cached data. Try deleting .data file.")
    files = os.listdir(history_directory)
    for f in files:
      self.parse_file(history_directory + '/' + f)

    if use_cache:
        # Dump parsed data to cache
        try:
            f = open(cache_file, "wb")
            pickle.dump( (self.messages, self.senders, self.calls ), f)
        except IOError:
            print("Could not open cache file for saving parsed data.")

  def parse_file(self, input_file_path):
    try:
      f = open(input_file_path)
    except IOError:
      print("Could not open input file %s." % input_file_path)
      sys.exit(1)
    
    metadata_lines = 0
    test_lines = 0 if SMALLER_SIZE else 100
    last_message = None
    print('starting to read file')
    for line in f:
      if metadata_lines < 2:
        metadata_lines = metadata_lines + 1
        continue

      line = line.strip()
      if not line:
        continue
      try:
        unused_date = datetime.strptime(line, '%A, %B %d, %Y')
        continue
      except ValueError:
        pass

      (dt, sender_name, text) = self.parse_line(line)
      if 'Voice Call' in text or 'Video Call' in text:
        call_info = text.split(" ")
        if len(call_info) < 3:
          continue
        try:
          exact_time = time.strptime(call_info[2], '%H:%M:%S')
        except ValueError:
          try:
            exact_time = time.strptime(call_info[2], '%M:%S')
          except ValueError:
            # Missed or cancled calls
            continue
  
        duration = timedelta(hours=exact_time.tm_hour,minutes=exact_time.tm_min,seconds=exact_time.tm_sec).total_seconds()
        call = Call(dt, duration, self.get_sender(sender_name), call_info[0] == 'Video')
        self.calls.append(call)
      if not dt and last_message:
        last_message.add_line(text)
      else:
        sender = self.get_sender(sender_name)
        if last_message and last_message.sender != sender:
          response_time = (dt - last_message.dt).total_seconds()
        else:
          response_time = 0
        message = Message(dt, sender, text, response_time)
        message.prev = last_message
        self.messages.append(message)
        last_message = message

      # test_lines = test_lines + 1
      # if test_lines > 500:
      #   break

  def parse_line(self, line):
    dt = None
    sender = ""
    text = line

    expected_messages = line.split(' :', 1)
    metadata = expected_messages[0].split(', ')
    if len(metadata) == 3:
      try:
        temp_date = metadata[0] + ' ' + metadata[1]
        temp_date = temp_date.replace('\u202f', ' ')
        dt = datetime.strptime(temp_date, '%b %d %Y at %I:%M %p')
        sender = metadata[2].strip()
        text = expected_messages[1].strip()
      except (ValueError, IndexError):
        pass

    return (dt, sender, text)

  def get_sender(self, name):
    try:
      sender = self.senders[name]
    except KeyError:
      sender = Sender(name)
      self.senders[name] = sender
    return sender

  def total_count(self):
      return len(self.messages)