package br.ws;

import jakarta.jws.WebService;
import jakarta.jws.WebMethod;
import jakarta.jws.WebParam;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import br.Project;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Victor Rizzo
 */
@WebService(serviceName = "Services")
public class SoapProjectManager {

    List<Project> projects = new ArrayList();

    private final Lock lock = new ReentrantLock();

    @WebMethod(operationName = "init")
    public String init(@WebParam(name = "projName") String PROJNAME) {
        lock.lock();
        try {
            try {
                System.out.println("Entrou no sleep");
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                Logger.getLogger(SoapProjectManager.class.getName()).log(Level.SEVERE, null, ex);
            }
            if (PROJNAME.isBlank()) {
                return "INIT FALHOU: Nome vazio";
            }

            Project newProj = new Project(PROJNAME, "");
            for (int i = 0; i < projects.size(); i++) {
                if (projects.get(i).getName().equals(PROJNAME)) {
                    return "INIT FALHOU: Projeto ja existe";
                }
            }
            projects.add(newProj);
            return "PROJETO CRIADO COM SUCESSO";
        } finally {
            System.out.println("Finalizou o processo");
            lock.unlock();
        }
    }

    @WebMethod(operationName = "commit")
    public String commit(@WebParam(name = "projName") String PROJNAME, @WebParam(name = "code") String CODE) {
        lock.lock();
        try {
            if (PROJNAME.isBlank()) {
                return "COMMIT FALHOU: Nome vazio";
            }
            
            for (int i = 0; i < projects.size(); i++) {
                if (projects.get(i).getName().equals(PROJNAME)) {
                    projects.get(i).setCode(CODE);
                    return "COMMIT FEITO COM SUCESSO";
                }
            }
            return "COMMIT FALHOU: Projeto nao encontrado";
        } finally {
            lock.unlock();
        }
    }

    @WebMethod(operationName = "clone")
    public String clone(@WebParam(name = "projName") String PROJNAME) {
        if (PROJNAME.isBlank()) {
            return "CLONE FALHOU: Nome vazio";
        }
        for (int i = 0; i < projects.size(); i++) {
            if (projects.get(i).getName().equals(PROJNAME)) {
                return projects.get(i).getCode();
            }
        }
        return "CLONE FALHOU: Projeto nao encontrado";
    }

    @WebMethod(operationName = "remove")
    public String remove(@WebParam(name = "projName") String PROJNAME) {
        lock.lock();
        try {
            if (PROJNAME.isBlank()) {
                return "REMOVE FALHOU: Nome vazio";
            }
            
            for (int i = 0; i < projects.size(); i++) {
                if (projects.get(i).getName().equals(PROJNAME)) {
                    projects.remove(i);
                    return "PROJETO REMOVIDO COM SUCESSO";
                }
            }
            return "REMOVE FALHOU: Projeto nao encontrado";
        } finally {
            lock.unlock();
        }
    }
}
