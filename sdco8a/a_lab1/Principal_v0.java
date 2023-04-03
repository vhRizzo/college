import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.concurrent.ThreadLocalRandom;
import java.io.FileWriter;

public class Principal_v0 {

    private final static String filePath = "fortune-br.txt";
    public final static Path path = Paths
            .get(filePath);

    private int NUM_FORTUNES = 0;

    public class FileReader {

        int teste;

        public int countFortunes() throws FileNotFoundException {

            int lineCount = 0;

            InputStream is = new BufferedInputStream(new FileInputStream(
                    path.toString()));
            try (BufferedReader br = new BufferedReader(new InputStreamReader(
                    is))) {

                String line = "";
                while (!(line == null)) {

                    if (line.equals("%"))
                        lineCount++;

                    line = br.readLine();

                } // fim while

                System.out.println(lineCount);
            } catch (IOException e) {
                System.out.println("SHOW: Excecao na leitura do arquivo.");
            }
            return lineCount;
        }

        public void parser(HashMap<Integer, String> hm)
                throws FileNotFoundException {

            InputStream is = new BufferedInputStream(new FileInputStream(
                    path.toString()));
            try (BufferedReader br = new BufferedReader(new InputStreamReader(
                    is))) {

                int lineCount = 0;

                String line = "";
                while (!(line == null)) {

                    if (line.equals("%"))
                        lineCount++;

                    line = br.readLine();
                    StringBuffer fortune = new StringBuffer();
                    while (!(line == null) && !line.equals("%")) {
                        fortune.append(line + "\n");
                        line = br.readLine();
                        // System.out.print(lineCount + ".");
                    }

                    hm.put(lineCount, fortune.toString());
                    System.out.println(fortune.toString());

                    System.out.println(lineCount);
                } // fim while

                teste = lineCount;

            } catch (IOException e) {
                System.out.println("SHOW: Excecao na leitura do arquivo.");
            }
        }

        public void read(HashMap<Integer, String> hm)
                throws FileNotFoundException {

            int numeroAleatorio = ThreadLocalRandom.current().nextInt(0, teste + 1);

            System.out.print("A frase a ser lida vai ser a de numero: " + numeroAleatorio);

            InputStream is = new BufferedInputStream(new FileInputStream(
                    path.toString()));
            try (BufferedReader br = new BufferedReader(new InputStreamReader(
                    is))) {

                int lineCount = 0;

                String line = "";
                while (!(line == null)) {

                    if (line.equals("%"))
                        lineCount++;

                    line = br.readLine();
                    StringBuffer fortune = new StringBuffer();
                    while (!(line == null) && !line.equals("%")) {
                        fortune.append(line + "\n");
                        line = br.readLine();
                        // System.out.print(lineCount + ".");
                    }

                    hm.put(lineCount, fortune.toString());

                    if (lineCount == numeroAleatorio) {

                        System.out.println(fortune.toString());

                    }

                }

            } catch (IOException e) {
                System.out.println("SHOW: Excecao na leitura do arquivo.");
            }

        }

        public void write(HashMap<Integer, String> hm)
                throws FileNotFoundException {
            String writeMessage = "Hello Guys";

            try {
                FileWriter escritor = new FileWriter(filePath, true);
                escritor.write(writeMessage + "\n%\n");
                escritor.close();
                System.out.println("Frase escrita com sucesso no arquivo " + filePath);
                System.out.println("Mensagem escrita: " + writeMessage);
            } catch (IOException e) {
                System.err.println("Erro ao escrever frase no arquivo " + filePath + ": " + e.getMessage());
            }

        }
    }

    public void iniciar() {

        FileReader fr = new FileReader();
        try {
            NUM_FORTUNES = fr.countFortunes();
            HashMap hm = new HashMap<Integer, String>();
            fr.parser(hm);
            fr.read(hm);
            fr.write(hm);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {
        new Principal_v0().iniciar();
    }

}