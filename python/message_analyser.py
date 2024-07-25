
from datetime import datetime
from analyser import Analyser
from objects import Message, Sender, Call

def get_longest_message(a, b):
  return b if a is None or len(a.words) < len(b.words) else a

class MessageAnalyser:
  analyser = {}
  messages_by_weekday = {}
  words_by_sender = {}
  
  def __init__(self, analyser):
    self.analyser = analyser
    for i in range(7):
      self.messages_by_weekday[i] = []
    
  def add_words_to_sender(self, message):
    for w in message.words:
      if w in self.words_by_sender:
        self.words_by_sender[w] = self.words_by_sender[w] + 1
      else:
        self.words_by_sender[w] = 1

  def get_message_stats(self):
    stats = {}
    messages_by_sender = {}
    longest_message_by_sender = {}
    word_count_by_sender = {}
    photos_by_sender = {}
    stickers_by_sender = {}
    laughs_by_sender = {}
    
    for i in range(7):
      self.messages_by_weekday[i] = []

    for s in self.analyser.senders.keys():
      messages_by_sender[s] = 0
      longest_message_by_sender[s] = None
      word_count_by_sender[s] = 0
      photos_by_sender[s] = 0
      stickers_by_sender[s] = 0
      laughs_by_sender[s] = 0

    for m in self.analyser.messages:
      self.messages_by_weekday[m.dt.weekday()].append(m)
      messages_by_sender[m.sender.name] = messages_by_sender[m.sender.name] + 1
      longest_message_by_sender[m.sender.name] = get_longest_message(longest_message_by_sender[m.sender.name], m)
      self.add_words_to_sender(m)
      word_count_by_sender[m.sender.name] = word_count_by_sender[m.sender.name] + len(m.words)
      if m.text == 'Photo':
        photos_by_sender[m.sender.name] = photos_by_sender[m.sender.name] + 1
      if m.text == 'Emoticons':
        stickers_by_sender[m.sender.name] = stickers_by_sender[m.sender.name] + 1
      if 'ㅋ' in m.text:
        laughs_by_sender[m.sender.name] = laughs_by_sender[m.sender.name] + 1
        
    
    longest_message_by_sender = {k: {'length': len(v.words), 'message': v.text} for k, v in longest_message_by_sender.items()}
    messages_by_weekday = {k: len(v) for k, v in self.messages_by_weekday.items()}
    
    stats = {
      'total_messages': len(self.analyser.messages),
      'total_messages_by_sender': messages_by_sender,
      'word_count_by_sender': word_count_by_sender,
      'photos_by_sender': photos_by_sender,
      'stickers_by_sender': stickers_by_sender,
      'laughs_by_sender': laughs_by_sender,
      'messages_by_weekday': messages_by_weekday,
      'longest_message_by_sender': longest_message_by_sender,
    } 
    
    return stats
    