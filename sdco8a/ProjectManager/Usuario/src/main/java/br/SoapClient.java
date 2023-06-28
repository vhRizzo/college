package br;

import jakarta.xml.soap.MessageFactory;
import jakarta.xml.soap.SOAPBody;
import jakarta.xml.soap.SOAPBodyElement;
import jakarta.xml.soap.SOAPConnection;
import jakarta.xml.soap.SOAPConnectionFactory;
import jakarta.xml.soap.SOAPElement;
import jakarta.xml.soap.SOAPEnvelope;
import jakarta.xml.soap.SOAPException;
import jakarta.xml.soap.SOAPMessage;
import jakarta.xml.soap.SOAPPart;
import javax.xml.namespace.QName;

/**
 *
 * @author Victor Rizzo
 */
public class SoapClient {

    private int method;
    private String projName;
    private String code;
    
    public static String callInit(String projName) {
        try {
            // Cria a mensagem SOAP
            SOAPMessage soapMessage = MessageFactory.newInstance().createMessage();
            SOAPPart soapPart = soapMessage.getSOAPPart();
            SOAPEnvelope soapEnvelope = soapPart.getEnvelope();
            soapEnvelope.addNamespaceDeclaration("web", "http://ws.br/");

            // Cria o corpo da mensagem SOAP
            SOAPBody soapBody = soapEnvelope.getBody();
            QName operationName = new QName("http://ws.br/", "init", "web");
            SOAPBodyElement initElement = soapBody.addBodyElement(operationName);

            // Adiciona o valor do parâmetro "projName" à mensagem SOAP
            QName projNameQName = new QName("projName");
            SOAPElement projNameElement = initElement.addChildElement(projNameQName);
            projNameElement.setValue(projName);
                    
            // Configura o endereço do servidor SOAP
            String serverUrl = "http://localhost:8080/ProjectManager/Services";

            // Envia a mensagem SOAP para o servidor e obtém a resposta
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();
            SOAPMessage soapResponse = soapConnection.call(soapMessage, serverUrl);

            // Extrai a resposta da mensagem SOAP
            SOAPBody soapResponseBody = soapResponse.getSOAPBody();
            String response = soapResponseBody.getTextContent();

            // Imprime a resposta
            System.out.println(response);

            // Fecha a conexão SOAP
            soapConnection.close();
            return response;
        } catch (SOAPException e) {
            e.printStackTrace();
        }
        return null;
    }
    
    public static String callCommit(String projName, String code) {
        try {
            // Cria a mensagem SOAP
            SOAPMessage soapMessage = MessageFactory.newInstance().createMessage();
            SOAPPart soapPart = soapMessage.getSOAPPart();
            SOAPEnvelope soapEnvelope = soapPart.getEnvelope();
            soapEnvelope.addNamespaceDeclaration("web", "http://ws.br/");

            // Cria o corpo da mensagem SOAP
            SOAPBody soapBody = soapEnvelope.getBody();
            QName operationName = new QName("http://ws.br/", "commit", "web");
            SOAPBodyElement initElement = soapBody.addBodyElement(operationName);

            // Adiciona o valor do parâmetro "projName" à mensagem SOAP
            QName projNameQName = new QName("projName");
            SOAPElement projNameElement = initElement.addChildElement(projNameQName);
            projNameElement.setValue(projName);

            // Adiciona o valor do parâmetro "code" à mensagem SOAP
            QName codeQName = new QName("code");
            SOAPElement codeElement = initElement.addChildElement(codeQName);
            codeElement.setValue(code);
                    
            // Configura o endereço do servidor SOAP
            String serverUrl = "http://localhost:8080/ProjectManager/Services";

            // Envia a mensagem SOAP para o servidor e obtém a resposta
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();
            SOAPMessage soapResponse = soapConnection.call(soapMessage, serverUrl);

            // Extrai a resposta da mensagem SOAP
            SOAPBody soapResponseBody = soapResponse.getSOAPBody();
            String response = soapResponseBody.getTextContent();

            // Imprime a resposta
            System.out.println(response);

            // Fecha a conexão SOAP
            soapConnection.close();
            return response;
        } catch (SOAPException e) {
            e.printStackTrace();
        }
        return null;
    }
    
    public static String callClone(String projName) {
        try {
            // Cria a mensagem SOAP
            SOAPMessage soapMessage = MessageFactory.newInstance().createMessage();
            SOAPPart soapPart = soapMessage.getSOAPPart();
            SOAPEnvelope soapEnvelope = soapPart.getEnvelope();
            soapEnvelope.addNamespaceDeclaration("web", "http://ws.br/");

            // Cria o corpo da mensagem SOAP
            SOAPBody soapBody = soapEnvelope.getBody();
            QName operationName = new QName("http://ws.br/", "clone", "web");
            SOAPBodyElement initElement = soapBody.addBodyElement(operationName);

            // Adiciona o valor do parâmetro "projName" à mensagem SOAP
            QName projNameQName = new QName("projName");
            SOAPElement projNameElement = initElement.addChildElement(projNameQName);
            projNameElement.setValue(projName);
                    
            // Configura o endereço do servidor SOAP
            String serverUrl = "http://localhost:8080/ProjectManager/Services";

            // Envia a mensagem SOAP para o servidor e obtém a resposta
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();
            SOAPMessage soapResponse = soapConnection.call(soapMessage, serverUrl);

            // Extrai a resposta da mensagem SOAP
            SOAPBody soapResponseBody = soapResponse.getSOAPBody();
            String response = soapResponseBody.getTextContent();

            // Imprime a resposta
            System.out.println(response);

            // Fecha a conexão SOAP
            soapConnection.close();
            return response;
        } catch (SOAPException e) {
            e.printStackTrace();
        }
        return null;
    }
    
    public static String callRemove(String projName) {
        try {
            // Cria a mensagem SOAP
            SOAPMessage soapMessage = MessageFactory.newInstance().createMessage();
            SOAPPart soapPart = soapMessage.getSOAPPart();
            SOAPEnvelope soapEnvelope = soapPart.getEnvelope();
            soapEnvelope.addNamespaceDeclaration("web", "http://ws.br/");

            // Cria o corpo da mensagem SOAP
            SOAPBody soapBody = soapEnvelope.getBody();
            QName operationName = new QName("http://ws.br/", "remove", "web");
            SOAPBodyElement initElement = soapBody.addBodyElement(operationName);

            // Adiciona o valor do parâmetro "projName" à mensagem SOAP
            QName projNameQName = new QName("projName");
            SOAPElement projNameElement = initElement.addChildElement(projNameQName);
            projNameElement.setValue(projName);
                    
            String serverUrl = "http://localhost:8080/ProjectManager/Services";

            // Envia a mensagem SOAP para o servidor e obtém a resposta
            SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
            SOAPConnection soapConnection = soapConnectionFactory.createConnection();
            SOAPMessage soapResponse = soapConnection.call(soapMessage, serverUrl);

            // Extrai a resposta da mensagem SOAP
            SOAPBody soapResponseBody = soapResponse.getSOAPBody();
            String response = soapResponseBody.getTextContent();

            // Imprime a resposta
            System.out.println(response);

            // Fecha a conexão SOAP
            soapConnection.close();
            return response;
        } catch (SOAPException e) {
            e.printStackTrace();
        }
        return null;
    }
}
