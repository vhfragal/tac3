import threading
import time

class MonitorFila:
    def __init__(self, limite_maximo=5):
        self.itens = []
        self.limite = limite_maximo
        self.lock = threading.Lock()
        self.pode_produzir = threading.Condition(self.lock)
        self.pode_consumir = threading.Condition(self.lock)

    def adicionar(self, item):
        with self.lock:
            # Espera se a fila estiver cheia
            while len(self.itens) >= self.limite:
                print(f"[Produtor] Fila cheia. Aguardando...")
                self.pode_produzir.wait()
            
            self.itens.append(item)
            print(f"[Produtor] Adicionou: {item} | Fila: {self.itens}")
            
            # Notifica que há um item disponível para consumo
            self.pode_consumir.notify()

    def remover(self):
        with self.lock:
            # Espera se a fila estiver vazia
            while len(self.itens) == 0:
                print(f"[Consumidor] Fila vazia. Aguardando...")
                self.pode_consumir.wait()
            
            item = self.itens.pop(0)
            print(f"[Consumidor] Removeu: {item} | Fila: {self.itens}")
            
            # Notifica que há espaço disponível na fila
            self.pode_produzir.notify()
            return item

# Testando o monitor com threads
def produtor(monitor):
    for i in range(5):
        time.sleep(0.5)
        monitor.adicionar(f"Dado-{i}")

def consumidor(monitor):
    for i in range(5):
        time.sleep(1)
        monitor.remover()

if __name__ == "__main__":
    fila_monitorada = MonitorFila(limite_maximo=3)
    
    t1 = threading.Thread(target=produtor, args=(fila_monitorada,))
    t2 = threading.Thread(target=consumidor, args=(fila_monitorada,))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
