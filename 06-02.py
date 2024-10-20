import threading
import time
import random

class MessageProducer(threading.Thread):
    def __init__(self,condition,data,buffer):
        super().__init__()
        self.condition=condition
        self.data=data
        self.buffer=buffer

    def run(self):
        n="text"
        i=0
        while ( i<self.buffer):
            time.sleep(random.uniform(0.5, 2))
            n=input("ingrese mensaje a escribir")
            with self.condition:
                self.data.append(n)
                i=i+1
                print(f"Productor produjo: {i}\n",end="")
                self.condition.notify()
        
class MessageConsumer(threading.Thread):
    def __init__(self, condition, data,buffer):
        super().__init__()
        self.condition = condition
        self.data = data
        self.buffer=buffer
    def run(self): 
        for i in range(0,self.buffer):
            with self.condition:                 
                while not self.data:             
                    self.condition.wait()        
                i=i+1
                item = self.data.pop(0)         
                print(f"Consumidor consumió: {i}{item}\n",end="")
            time.sleep(random.uniform(0.5, 2))   



def main():
    condition = threading.Condition()           
    data = []
    len=[]                                   

    producer =MessageProducer(condition, data,3)         
    consumer =MessageConsumer(condition, data,3)         

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("Producción y consumo han finalizado.",end="")

if __name__ == "__main__":
    main()