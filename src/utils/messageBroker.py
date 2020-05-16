import threading, os

class MessageBroker:
    
    def __init__(self, threads=os.cpu_count()):
        self._topics = {}
    
    def sub(self, topic, subscriber):
        if not topic in self._topics:
            self._topics[topic] = []
        
        self._topics[topic].append(subscriber)

    def unsub(self, topic, subscriber):
        if topic in self._topics:
            self._topics[topic].remove(subscriber)
    
    def publish(self, topic, *args, **kwargs):
        if not topic in self._topics:
            return
        
        for subscriber in self._topics[topic]:
            thread = threading.Thread(target=subscriber, args=args, kwargs=kwargs)
            thread.start()