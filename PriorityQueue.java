/**
 * Interfaz que define las operaciones de una cola con prioridad.
 * @param <E> Tipo de elemento que será almacenado en la cola
 */
public interface PriorityQueue<E extends Comparable<E>> {
    
    /**
     * Inserta un elemento en la cola con prioridad.
     * @param elemento Elemento a insertar
     */
    public void add(E elemento);
    
    /**
     * Retorna el elemento con mayor prioridad sin removerlo.
     * @return Elemento con mayor prioridad
     */
    public E getFirst();
    
    /**
     * Remueve y retorna el elemento con mayor prioridad.
     * @return Elemento con mayor prioridad
     */
    public E remove();
    
    /**
     * Verifica si la cola está vacía.
     * @return true si la cola está vacía, false en caso contrario
     */
    public boolean isEmpty();
    
    /**
     * Retorna el tamaño de la cola.
     * @return número de elementos en la cola
     */
    public int size();

    public void clear();
}