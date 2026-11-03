class Event:
    def __init__(self, type:int, value:object):
        self.type = type
        self.value = value


class Notify:
    def __init__(self):
        self.events:list[Event] = []
    
    def add_event(self, type:int, value):
        self.events.append(Event(type, value))

    def get_events(self):        
        return self.events

    def clear(self):
        self.events = []

notify = Notify()


