import java.util.Vector;

/**
 * Implementación de una cola con prioridad basada en un heap.
 * @param <E> Tipo de elemento que será almacenado en la cola
 */
public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    protected Vector<E> data; // vector que almacena los elementos
    
    public VectorHeap() {
        data = new Vector<E>();
    }
    
    /**
     * Constructor que inicializa el heap con los elementos de un vector.
     * @param v Vector con elementos iniciales
     */
    public VectorHeap(Vector<E> v) {
        data = new Vector<E>(v.size()); // se crea con capacidad suficiente
        for (E elemento : v) {
            add(elemento);
        }
    }
    
    /**
     * Retorna la posición del padre de un nodo en el heap.
     * @param i Posición del nodo
     * @return Posición del padre
     */
    protected int parent(int i) {
        return (i - 1) / 2;
    }
    
    /**
     * Retorna la posición del hijo izquierdo de un nodo en el heap.
     * @param i Posición del nodo
     * @return Posición del hijo izquierdo
     */
    protected int left(int i) {
        return 2 * i + 1;
    }
    
    /**
     * Retorna la posición del hijo derecho de un nodo en el heap.
     * @param i Posición del nodo
     * @return Posición del hijo derecho
     */
    protected int right(int i) {
        return 2 * i + 2;
    }
    
    /**
     * Mueve un nodo hacia arriba en el heap hasta su posición correcta.
     * @param leaf Posición del nodo a mover
     */
    protected void percolateUp(int leaf) {
        int parent = parent(leaf);
        E value = data.get(leaf);

        while (leaf > 0 && value.compareTo(data.get(parent)) < 0) {
            data.set(leaf, data.get(parent));
            leaf = parent;
            parent = parent(leaf);
        }
        
        data.set(leaf, value);
    }
    
    /**
     * Mueve un nodo hacia abajo en el heap hasta su posición correcta.
     * @param root Posición del nodo a mover
     */
    protected void pushDownRoot(int root) {
        int heapSize = data.size();
        E value = data.get(root);
        
        while (root < heapSize) {
            int childpos = left(root);
            
            if (childpos >= heapSize) {
                break;
            }
            
            if (right(root) < heapSize && 
                data.get(right(root)).compareTo(data.get(childpos)) < 0) {
                childpos = right(root);
            }

            if (value.compareTo(data.get(childpos)) <= 0) {
                break;
            }

            data.set(root, data.get(childpos));
            root = childpos;
        }
        
        data.set(root, value);
    }
    
    /**
     * Añade un elemento al heap.
     * @param value Elemento a añadir
     */
    @Override
    public void add(E value) {
        data.add(value);
        percolateUp(data.size() - 1);
    }
    
    /**
     * Retorna el elemento con mayor prioridad sin removerlo.
     * @return Elemento con mayor prioridad
     */
    @Override
    public E getFirst() {
        if (isEmpty()) {
            return null;
        }
        return data.get(0);
    }
    
    /**
     * Remueve y retorna el elemento con mayor prioridad.
     * @return Elemento con mayor prioridad
     */
    @Override
    public E remove() {
        if (isEmpty()) {
            return null;
        }
        
        E minValue = getFirst();
        data.set(0, data.get(data.size() - 1));
        data.setSize(data.size() - 1);
        
        if (data.size() > 0) {
            pushDownRoot(0);
        }
        
        return minValue;
    }
    
    /**
     * Verifica si el heap está vacío.
     * @return true si está vacío, false en caso contrario
     */
    @Override
    public boolean isEmpty() {
        return data.size() == 0;
    }
    
    /**
     * Retorna el tamaño del heap.
     * @return número de elementos en el heap
     */
    @Override
    public int size() {
        return data.size();
    }
    
    @Override
    public void clear() {
        data.clear();
    }
}