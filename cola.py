class Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox

    def __str__(self):
        return str(self.dato)


class Cola:
    """Representa a una cola, con operaciones de encolar y
       desencolar. El primero en ser encolado es también el primero
       en ser desencolado. """

    def __init__(self):
        """Crea una cola vacía."""
        self.primero = None
        self.ultimo = None

    def __str__(self):
        """ Imprime el contenido de la lista. """
        nodo = self.primero
        s = "["
        while nodo is not None:
            if len(s) > 1:
                s += ", "
            s += str(nodo)
            nodo = nodo.prox
        s += "]"
        return s

    def encolar(self, x):
        """Encola el elemento x."""
        nuevo = Nodo(x)
        if self.ultimo:
            self.ultimo.prox = nuevo
            self.ultimo = nuevo
        else:
            self.primero = nuevo
            self.ultimo = nuevo

    def desencolar(self):
        """Desencola el primer elemento y devuelve su
           valor. Si la cola está vacía, levanta ValueError."""
        if self.primero is None:
            raise ValueError("La cola está vacía")
        valor = self.primero.dato
        self.primero = self.primero.prox
        if not self.primero:
            self.ultimo = None
        return valor

    def ver_primero(self):
        if not self.primero:
            return ValueError
        return self.primero.dato

    def esta_vacia(self):
        """Devuelve True si la cola esta vacía, False si no."""
        return self.primero is None
