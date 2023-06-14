
/**
 * Lab05: Sistema P2P
 * 
 * Autor: Lucio A. Rocha
 * Ultima atualizacao: 22/05/2023
 * 
 * Referencias: 
 * https://docs.oracle.com/javase/tutorial/essential/io
 * http://fortunes.cat-v.org/
 */

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Peer implements IMensagem {

	ArrayList<PeerLista> alocados;

	public Peer() {
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
		String result = "false";

		String fortune = "-1";

		String[] v = json.split(":");
		System.out.println(">>>" + v[1]);
		String[] v1 = v[1].split("\"");
		System.out.println(">>>" + v1[1]);
		if (v1[1].equals("write")) {
			String[] p = json.split("\\[");
			System.out.println(p[1]);
			String[] p1 = p[1].split("]");
			System.out.println(p1[0]);
			String[] p2 = p1[0].split("\"");
			System.out.println(p2[1]);
			fortune = p2[1];

			// Write in file
			Principal pv2 = new Principal();
			pv2.write(fortune);
		} else if (v1[1].equals("read")) {
			// Read file
			Principal pv2 = new Principal();
			fortune = pv2.read();
		}

		result = "{\n" + "\"result\": \"" + fortune + "\"" + "}";
		System.out.println(result);

		return result;
	}

	public void iniciar() {

		try {
			// Adquire aleatoriamente um ID do PeerList
			List<PeerLista> listaPeers = new ArrayList<>();
			for (PeerLista peer : PeerLista.values())
				listaPeers.add(peer);

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

			PeerLista peer = listaPeers.get(0);
			Scanner scanner = new Scanner(System.in);

			int tentativas = 0;
			boolean repetido = true;
			boolean cheio = false;
			do {
				System.out.println("Selecione um peer para se conectar:");
				for (int i = 1; i <= listaPeers.size(); i++)
					System.out.println(i + " - " + listaPeers.get(i - 1));

				boolean isInt = true;
				int opt = -1;

				try {
					opt = scanner.nextInt();
				} catch (Exception e) {
					scanner = new Scanner(System.in);
					isInt = false;
				}

				if (opt > listaPeers.size() || opt < 1 || !isInt) {
					System.out.println("Opcao invalida. Selecione uma opcao na lista.");
				} else {
					repetido = false;
					peer = listaPeers.get(opt - 1);

					for (int i = 0; i < listaAlocados.length && !repetido; i++) {

						if (listaAlocados[i].equals(peer.getNome())) {
							System.out.println(peer.getNome() + " ativo. Escolha outro...");
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
			} while (repetido && !cheio);

			if (cheio) {
				System.out.println("Sistema cheio. Tente mais tarde.");
				System.exit(1);
			}

			IMensagem skeleton = (IMensagem) UnicastRemoteObject.exportObject(this, 0); // 0: sistema operacional indica
																						// a porta (porta anonima)

			servidorRegistro.rebind(peer.getNome(), skeleton);
			System.out.print(peer.getNome() + " Servidor RMI: Aguardando conexoes...");

			// ---Cliente RMI
			new ClienteRMI().iniciarCliente();
			System.exit(0);

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	public static void main(String[] args) {
		Peer servidor = new Peer();
		servidor.iniciar();
	}
}
