package br;

import javafx.scene.control.Label;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField; // Import the TextField class
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

/**
 *
 * @author Victor Rizzo
 */
public class UsuarioMenu extends Application {

    private TextArea codeTextArea;
    private TextField nameTextField;
    private Label promptLabel;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Interface de Usuário");

        BorderPane mainPane = new BorderPane();

        // TextField para o nome do projeto
        nameTextField = new TextField();
        nameTextField.setPromptText("Digite o nome do projeto");
        
        // TextArea para digitar o código
        codeTextArea = new TextArea();
        codeTextArea.setPrefRowCount(10);
        codeTextArea.setPrefColumnCount(40);

        // Painel de botões
        HBox buttonPanel = new HBox(10);
        buttonPanel.setPadding(new Insets(10));

        // Botões
        Button button1 = new Button("Init");
        Button button2 = new Button("Commit");
        Button button3 = new Button("Clone");
        Button button4 = new Button("Remove");

        // Ação dos botões
        button1.setOnAction(event -> {
            updatePrompt(SoapClient.callInit(nameTextField.getText()));
        });

        button2.setOnAction(event -> {
            updatePrompt(SoapClient.callCommit(nameTextField.getText(), codeTextArea.getText()));
        });

        button3.setOnAction(event -> {
            String cloneResponse = SoapClient.callClone(nameTextField.getText());
            if (cloneResponse.contains("FALHOU")) {
                updatePrompt(cloneResponse);
            } else {
                updatePrompt("CLONE FEITO COM SUCESSO");
                codeTextArea.setText(cloneResponse);
            }
        });

        button4.setOnAction(event -> {
            updatePrompt(SoapClient.callRemove(nameTextField.getText()));
        });

        buttonPanel.getChildren().addAll(button1, button2, button3, button4);
        
        // Prompt Label
        promptLabel = new Label(" "); // Create the Label instance
        StackPane.setAlignment(promptLabel, Pos.BOTTOM_RIGHT); // Align to bottom right corner
        StackPane.setMargin(promptLabel, new Insets(0, 10, 10, 0)); // Add some margin
        StackPane stackPane = new StackPane(promptLabel); // Create a StackPane to hold the Label
        
// Create a new BorderPane for buttonPanel and stackPane
        BorderPane bottomPane = new BorderPane();
        bottomPane.setLeft(buttonPanel);
        bottomPane.setRight(stackPane);
        
        mainPane.setTop(nameTextField);
        mainPane.setCenter(codeTextArea);
        mainPane.setBottom(bottomPane);

        Scene scene = new Scene(mainPane, 600, 400);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
    
    private void updatePrompt(String promptText) {
        promptLabel.setText(promptText);

        if (promptText.contains("FALHOU")) {
            promptLabel.setStyle("-fx-text-fill: red;");
        } else {
            promptLabel.setStyle("-fx-text-fill: green;");
        }
    }
}
