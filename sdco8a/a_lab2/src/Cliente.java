
/**
 * Laboratorio 1 de Sistemas Distribuidos
 * 
 * Autor: Lucio A. Rocha
 * Ultima atualizacao: 17/12/2022
 */

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class Cliente {

    private static Socket socket;
    private static DataInputStream entrada;
    private static DataOutputStream saida;

    private int porta = 1025;

    public void iniciar() {
        System.out.println("Cliente iniciado na porta: " + porta);

        try {

            socket = new Socket("127.0.0.1", porta);

            entrada = new DataInputStream(socket.getInputStream());
            saida = new DataOutputStream(socket.getOutputStream());

            // Recebe do usuario algum valor
            int valor = -1;
            do {
                BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                System.out.print(
                        "\nEscolha uma opcao:\n1 - Ler uma fortuna\n2 - Criar uma nova fortuna\n\nSua escolha: ");
                valor = Integer.parseInt(br.readLine());
                switch (valor) {
                    case 1:
                        read();
                        break;
                    case 2:
                        write();
                        break;
                    default:
                        System.out.println("Escolha invalida");
                        break;
                }
            } while (valor != 1 && valor != 2);

            socket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void read() {
        String json = "{\n\"method\": \"read\"\n\"args\": [\"\"]\n}";
        String resultado = new String();
        try {
            // O valor eh enviado ao servidor
            saida.writeUTF(json);
            // Recebe-se o resultado do servidor
            resultado = entrada.readUTF();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Mostra o resultado na tela
        System.out.println(resultado);
    }

    public static void write() {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Digite a mensagem que deseja inserir: ");

        String resultado = new String();
        try {
            String input = br.readLine();

            String json = "{\n\"method\": \"write\"\n\"args\": [\"" + input + "\"]\n}";
            // O valor eh enviado ao servidor
            saida.writeUTF(json);

            // Recebe-se o resultado do servidor
            resultado = entrada.readUTF();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Mostra o resultado na tela
        System.out.println(resultado);
    }

    public static void main(String[] args) {
        new Cliente().iniciar();
    }
}
