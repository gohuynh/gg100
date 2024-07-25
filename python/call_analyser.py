
from datetime import datetime
from analyser import Analyser
from objects import Message, Sender, Call

class CallAnalyser:
  analyser = {}
  calls_by_weekday = {}
  
  def __init__(self, analyser):
    self.analyser = analyser
    for i in range(7):
      self.calls_by_weekday[i] = []

  def get_call_stats(self):
    stats = {}
    total_duration = 0
    total_video_duration = 0
    num_video_calls = 0
    duration_by_sender = {}
    calls_by_sender = {}
    longest_call = 0
    longest_video_call = 0
    for s in self.analyser.senders.keys():
      duration_by_sender[s] = 0
      calls_by_sender[s] = 0
    for c in self.analyser.calls:
      self.calls_by_weekday[c.dt.weekday()].append(c)
      total_duration = total_duration + c.duration
      if c.is_video:
        total_video_duration = total_video_duration + c.duration
        num_video_calls = num_video_calls + 1
      duration_by_sender[c.sender.name] = duration_by_sender[c.sender.name] + c.duration
      calls_by_sender[c.sender.name] = calls_by_sender[c.sender.name] + 1
      longest_call = c.duration if c.duration > longest_call else longest_call
      longest_video_call = c.duration if c.duration > longest_video_call and c.is_video else longest_video_call
    
    calls_by_weekday = {}
    for i in range(7):
      calls_by_weekday[i] = len(self.calls_by_weekday[i])
    
    stats = {
      'total_duration': total_duration,
      'total_video_duration': total_video_duration,
      'total_calls': len(self.analyser.calls),
      'total_video_calls': num_video_calls,
      'duration_by_sender': duration_by_sender,
      'calls_by_sender': calls_by_sender,
      'longest_call': longest_call,
      'longest_video_call': longest_video_call,
      'calls_by_weekday': calls_by_weekday
    }
    return stats
    