class Pila: 
    def __init__(self): 
        self.items = []
    
    def ver_tope(self):
        return self.items[-1]

    def apilar(self, dato): 
        self.items.append(dato)
    
    def desapilar(self): 
        if self.esta_vacia(): 
            raise ValueError("La pila esta vacia")
        return self.items.pop() 
    
    def esta_vacia(self): 
        return len(self.items) == 0
        
    def __str__(self):
        '''
        Devuelve una representación de la pila en la forma: 
        | e1, e2, ..., <TOPE
        '''
        return '| ' + ', '.join(map(str, self.items)) + ' <TOPE'
