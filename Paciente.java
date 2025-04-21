public class Paciente implements Comparable<Paciente> {
    private String nombre;
    private String sintoma;
    private char codigoEmergencia;
    
    /**
     * Constructor de la clase Paciente.
     * @param nombre Nombre del paciente
     * @param sintoma Descripción del síntoma
     * @param codigoEmergencia Código de emergencia (A-E)
     */
    public Paciente(String nombre, String sintoma, char codigoEmergencia) {
        this.nombre = nombre;
        this.sintoma = sintoma;
        this.codigoEmergencia = codigoEmergencia;
    }
    
    /**
     * Método compareTo para determinar la prioridad entre pacientes.
     * Los códigos de emergencia van de A (más urgente) a E (menos urgente).
     * @param otro Paciente con el que se compara
     * @return valor negativo si este paciente tiene mayor prioridad, 
     *         positivo si tiene menor prioridad, 0 si es igual
     */
    @Override
    public int compareTo(Paciente otro) {
        return this.codigoEmergencia - otro.codigoEmergencia;
    }
    
    /**
     * Obtiene el nombre del paciente.
     * @return nombre del paciente
     */
    public String getNombre() {
        return nombre;
    }
    
    /**
     * Obtiene el síntoma del paciente.
     * @return síntoma del paciente
     */
    public String getSintoma() {
        return sintoma;
    }
    
    /**
     * Obtiene el código de emergencia del paciente.
     * @return código de emergencia
     */
    public char getCodigoEmergencia() {
        return codigoEmergencia;
    }
    
    /**
     * Representación en String del paciente.
     * @return String con la información del paciente
     */
    @Override
    public String toString() {
        return nombre + ", " + sintoma + ", " + codigoEmergencia;
    }
}