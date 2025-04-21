import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.PriorityQueue;

public class SistemaEmergenciasJCF {
    
    /**
     * Método principal del sistema.
     * @param args argumentos de línea de comandos
     */
    public static void main(String[] args) {
        PriorityQueue<Paciente> colaPacientes = new PriorityQueue<>();

        try (BufferedReader br = new BufferedReader(new FileReader("pacientes.txt"))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                String[] datos = linea.split(",");
                if (datos.length == 3) {
                    String nombre = datos[0].trim();
                    String sintoma = datos[1].trim();
                    char codigo = datos[2].trim().charAt(0);

                    Paciente paciente = new Paciente(nombre, sintoma, codigo);
                    colaPacientes.add(paciente);
                }
            }
        } catch (IOException e) {
            System.err.println("Error al leer el archivo de pacientes: " + e.getMessage());
            return;
        }
        
        System.out.println("--- Sistema de Atención de Emergencias con Java Collection Framework ---");
        System.out.println("Pacientes registrados: " + colaPacientes.size());
        System.out.println("\nOrden de atención:");

        while (!colaPacientes.isEmpty()) {
            Paciente paciente = colaPacientes.poll(); 
            System.out.println(paciente);
        }
    }
}