
/**
  * Laboratorio 4  
  * Autor: Lucio Agostinho Rocha
  * Ultima atualizacao: 04/04/2023
  */
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class ServidorImpl implements IMensagem {

	ArrayList<Peer> alocados;

	public ServidorImpl() {
		alocados = new ArrayList<>();
	}

	// Cliente: invoca o metodo remoto 'enviar'
	// Servidor: invoca o metodo local 'enviar'
	@Override
	public Mensagem enviar(Mensagem mensagem) throws RemoteException {
		Mensagem resposta;
		try {
			System.out.println("Mensagem recebida: " + mensagem.getMensagem());
			resposta = new Mensagem(parserJSON(mensagem.getMensagem()));
		} catch (Exception e) {
			e.printStackTrace();
			resposta = new Mensagem("{\n" + "\"result\": false\n" + "}");
		}
		return resposta;
	}

	public String parserJSON(String json) {

		String result = new String();

		String list[] = json.split("\""); /*
											 * Para nao precisar incluir uma biblioteca externa, eu apenas dividi o JSON
											 * em todas as ocorrencias de aspas, desta forma o metodo ficara na posicao
											 * 3 da lista gerada, e os argumentos na posicao 7
											 */
		Path inputPath = Paths.get("src/fortunes_openbsd.txt"); // Abre o arquivo de entrada
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
					result = "{\n\"result\": \"" + tmp + "\n\"\n}"; // Gera o JSON de retorno
				} catch (IOException e) {
					e.printStackTrace();
				}
				break;
			case "write":
				String args = list[7];
				result = "{\n\"result\": \"" + args + "\n\"\n}"; // Gera o JSON de retorno
				try {
					Files.write(inputPath, new String(args + "\n%\n").getBytes(), StandardOpenOption.APPEND);
				} catch (IOException e) {
					e.printStackTrace();
				}
				break;
			default: // Os metodos sao autogerados pelo algoritmo, entao nao deve haver nenhum erro
				break; // para cair no default
		}

		return result;

	}

	public void iniciar() {

		try {

			List<Peer> listaPeers = Arrays.asList(Peer.values());

			Registry servidorRegistro;
			try {
				servidorRegistro = LocateRegistry.createRegistry(1099);
			} catch (java.rmi.server.ExportException e) { // Registro jah iniciado
				System.out.print("Registro jah iniciado. Usar o ativo.\n");
			}
			servidorRegistro = LocateRegistry.getRegistry(); // Registro eh unico para todos os peers
			String[] listaAlocados = servidorRegistro.list();
			for (int i = 0; i < listaAlocados.length; i++)
				System.out.println(listaAlocados[i] + " ativo.");

			SecureRandom sr = new SecureRandom();
			Peer peer = listaPeers.get(sr.nextInt(listaPeers.size()));

			int tentativas = 0;
			boolean repetido = true;
			boolean cheio = false;
			while (repetido && !cheio) {
				repetido = false;
				peer = listaPeers.get(sr.nextInt(listaPeers.size()));
				for (int i = 0; i < listaAlocados.length && !repetido; i++) {

					if (listaAlocados[i].equals(peer.getNome())) {
						System.out.println(peer.getNome() + " ativo. Tentando proximo...");
						repetido = true;
						tentativas = i + 1;
					}

				}
				// System.out.println(tentativas+" "+listaAlocados.length);

				// Verifica se o registro estah cheio (todos alocados)
				if (listaAlocados.length > 0 && // Para o caso inicial em que nao ha servidor alocado,
												// caso contrario, o teste abaixo sempre serah true
						tentativas == listaPeers.size()) {
					cheio = true;
				}
			}

			if (cheio) {
				System.out.println("Sistema cheio. Tente mais tarde.");
				System.exit(1);
			}

			IMensagem skeleton = (IMensagem) UnicastRemoteObject.exportObject(this, 0); // 0: sistema operacional indica
																						// a porta (porta anonima)
			servidorRegistro.rebind(peer.getNome(), skeleton);
			System.out.print(peer.getNome() + " Servidor RMI: Aguardando conexoes...");

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	public static void main(String[] args) {
		ServidorImpl servidor = new ServidorImpl();
		servidor.iniciar();
	}
}
