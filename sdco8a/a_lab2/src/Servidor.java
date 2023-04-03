import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Random;

public class Servidor {

	private static Socket socket;
	private static ServerSocket server;

	private static DataInputStream entrada;
	private static DataOutputStream saida;

	private int porta = 1025;

	public void iniciar() {
		System.out.println("Servidor iniciado na porta: " + porta);
		try {

			// Criar porta de recepcao
			server = new ServerSocket(porta);
			socket = server.accept(); // Processo fica bloqueado, ah espera de conexoes

			// Criar os fluxos de entrada e saida
			entrada = new DataInputStream(socket.getInputStream());
			saida = new DataOutputStream(socket.getOutputStream());

			// Recebimento da String
			String input = entrada.readUTF();
			System.out.println(input);

			// Processamento do valor
			String resultado = parser(input);

			// Envio dos dados (resultado)
			saida.writeUTF(resultado);

			socket.close();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static String parser(String input) {
		String list[] = input.split("\""); /*
											 * Para nao precisar incluir uma biblioteca externa, eu apenas dividi o JSON
											 * em todas as ocorrencias de aspas, desta forma o metodo ficara na posicao
											 * 3 da lista gerada, e os argumentos na posicao 7
											 */
		String resultado = new String(); // String de retorno
		Path inputPath = Paths.get("src/fortune-br.txt"); // Abre o arquivo de entrada
		switch (list[3]) {
			case "read":
				Charset charset = StandardCharsets.UTF_8; // Charset para fazer a leitura do arquivo
				String content = new String(); // String para armazenar o conteudo do arquivo
				Random rng = new Random(); // Gerador de numeros aleatorios

				try {
					content = new String(Files.readAllBytes(inputPath), charset); // Armazena o conteudo do arquivo em
																					// uma string
					String fortuneList[] = content.split("\n%"); /*
																	 * Ao dividir a string em ocorrências de "\n%"
																	 * garente-se que somente os delimitadores serao
																	 * divididos, e nao os '%' utilizado no corpo de
																	 * algumas fortunas
																	 */

					String tmp = fortuneList[rng.nextInt(fortuneList.length)]; // Gera um numero aleatorio e exibe a
																				// string na posicao desse numero
					resultado = "{\n\"result\": \"" + tmp + "\n\"\n}"; // Gera o JSON de retorno
				} catch (IOException e) {
					e.printStackTrace();
				}
				break;
			case "write":
				String args = list[7];
				resultado = "{\n\"result\": \"" + args + "\n\"\n}"; // Gera o JSON de retorno
				try {
					Files.write(inputPath, new String(args + "\n%\n").getBytes(), StandardOpenOption.APPEND);
				} catch (IOException e) {
					e.printStackTrace();
				}
				break;
			default: // Os metodos sao autogerados pelo algoritmo, entao nao deve haver nenhum erro
				break; // para cair no default
		}
		return resultado;
	}

	public static void main(String[] args) {
		new Servidor().iniciar();
	}
}
