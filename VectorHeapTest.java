import org.junit.Test;
import static org.junit.Assert.*;
import org.junit.Before;

/**
 * Pruebas unitarias para la clase VectorHeap
 */
public class VectorHeapTest {
    
    private VectorHeap<Integer> heap;
    
    /**
     * Configuración previa a cada prueba.
     */
    @Before
    public void setUp() {
        heap = new VectorHeap<>();
    }
    
    /**
     * Prueba para el método isEmpty en un heap vacío.
     */
    @Test
    public void testIsEmptyOnNewHeap() {
        assertTrue("Un heap nuevo debe estar vacío", heap.isEmpty());
        assertEquals("Un heap nuevo debe tener tamaño 0", 0, heap.size());
    }
    
    /**
     * Prueba para los métodos add y size.
     */
    @Test
    public void testAddAndSize() {
        heap.add(5);
        assertFalse("El heap no debe estar vacío después de añadir", heap.isEmpty());
        assertEquals("El tamaño debe ser 1 después de añadir un elemento", 1, heap.size());
        
        heap.add(3);
        heap.add(7);
        assertEquals("El tamaño debe ser 3 después de añadir tres elementos", 3, heap.size());
    }
    
    /**
     * Prueba para el método getFirst en un heap con elementos.
     */
    @Test
    public void testGetFirst() {
        heap.add(5);
        heap.add(3);
        heap.add(7);
        
        assertEquals("getFirst debe devolver el elemento con mayor prioridad", Integer.valueOf(3), heap.getFirst());
        assertEquals("El tamaño no debe cambiar después de getFirst", 3, heap.size());
    }
    
    /**
     * Prueba para el método remove.
     */
    @Test
    public void testRemove() {
        heap.add(5);
        heap.add(3);
        heap.add(7);
        
        assertEquals("Remove debe devolver el elemento con mayor prioridad", Integer.valueOf(3), heap.remove());
        assertEquals("El tamaño debe disminuir después de remove", 2, heap.size());
        assertEquals("El nuevo elemento con mayor prioridad debe ser el siguiente", Integer.valueOf(5), heap.getFirst());
    }
    
    /**
     * Prueba para verificar el orden de extracción de elementos.
     */
    @Test
    public void testExtractInOrder() {
        // Añadir elementos en orden aleatorio
        heap.add(10);
        heap.add(4);
        heap.add(15);
        heap.add(7);
        heap.add(2);
        heap.add(20);
        
        // Verificar que se extraen en orden de prioridad (de menor a mayor para Integer)
        assertEquals(Integer.valueOf(2), heap.remove());
        assertEquals(Integer.valueOf(4), heap.remove());
        assertEquals(Integer.valueOf(7), heap.remove());
        assertEquals(Integer.valueOf(10), heap.remove());
        assertEquals(Integer.valueOf(15), heap.remove());
        assertEquals(Integer.valueOf(20), heap.remove());
        
        // Verificar que el heap está vacío
        assertTrue("El heap debe estar vacío después de extraer todos los elementos", heap.isEmpty());
    }
    
    /**
     * Prueba para el método clear.
     */
    @Test
    public void testClear() {
        heap.add(5);
        heap.add(3);
        heap.add(7);
        
        heap.clear();
        assertTrue("El heap debe estar vacío después de clear", heap.isEmpty());
        assertEquals("El tamaño debe ser 0 después de clear", 0, heap.size());
    }
    
    /**
     * Prueba para getFirst en un heap vacío.
     */
    @Test
    public void testGetFirstOnEmptyHeap() {
        assertNull("getFirst debe devolver null en un heap vacío", heap.getFirst());
    }
    
    /**
     * Prueba para remove en un heap vacío.
     */
    @Test
    public void testRemoveOnEmptyHeap() {
        assertNull("remove debe devolver null en un heap vacío", heap.remove());
    }
    
    /**
     * Prueba con la clase Paciente para verificar la comparación personalizada.
     */
    @Test
    public void testPacientePriorities() {
        VectorHeap<Paciente> pacienteHeap = new VectorHeap<>();
        
        Paciente p1 = new Paciente("Juan Perez", "fractura de pierna", 'C');
        Paciente p2 = new Paciente("Maria Ramirez", "apendicitis", 'A');
        Paciente p3 = new Paciente("Lorenzo Toledo", "chikunguya", 'E');
        Paciente p4 = new Paciente("Carmen Sarmientos", "dolores de parto", 'B');
        
        pacienteHeap.add(p1);
        pacienteHeap.add(p2);
        pacienteHeap.add(p3);
        pacienteHeap.add(p4);
        
        // Verificar que se extraen en orden de prioridad (A, B, C, E)
        assertEquals("Maria Ramirez", pacienteHeap.remove().getNombre());
        assertEquals("Carmen Sarmientos", pacienteHeap.remove().getNombre());
        assertEquals("Juan Perez", pacienteHeap.remove().getNombre());
        assertEquals("Lorenzo Toledo", pacienteHeap.remove().getNombre());
    }
}