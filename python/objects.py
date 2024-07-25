
from collections import Counter

class Message:
  dt = None
  response_time = 0
  text = ""
  sender = None
  prev = None
  words = []

  def __init__(self, dt, sender, text, response_time):
      self.dt = dt
      self.sender = sender
      self.text = text
      self.response_time = response_time
      self.words = text.split(" ")

  def add_line(self, text):
      self.text = self.text + "\n" + text

  def count_words(self):
      return len(re.findall(r'\b\w+\b', self.text))

  def __str__(self):
      return "[%s] %s: %s" % (self.dt, self.sender.name, self.text)

class Call:
  dt = None
  duration = 0
  sender = None
  is_video = False

  def __init__(self, dt, duration, sender, is_video):
      self.dt = dt
      self.duration = duration
      self.sender = sender
      self.is_video = is_video

  def __str__(self):
      return "[%s] %s: Called for %s, is_video: %s" % (self.dt, self.sender.name, str(timedelta(seconds=self.duration)), self.is_video)

class Sender:
    name = ""
    count = Counter(messages=0, words=0)
    response_time = Counter(time=0, count=0)
    calls = Counter(calls=0, duration=0, video=0)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def count_message(self, message):
        self.count = self.count + Counter(messages=1, words=message.count_words())

    def count_caller(self, call):
        self.calls = self.calls + Counter(calls=1, duration=call.duration, video=1 if call.is_video else 0)
