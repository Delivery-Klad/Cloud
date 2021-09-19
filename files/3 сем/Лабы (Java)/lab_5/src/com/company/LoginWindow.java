package com.company;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class LoginWindow extends JFrame{
    private JLabel labelLogin = new JLabel("Логин: ");
    private JLabel labelPassword = new JLabel("Пароль: ");
    private JTextField inputLogin = new JTextField("");
    private JTextField inputPassword = new JTextField("");
    private JButton buttonEnter = new JButton("Войти");
    private JButton buttonRegistration = new JButton("Регистрация");

    LoginWindow() {
        super("Меню авторизации");
        Dimension dim = getToolkit().getScreenSize();
        this.setBounds(dim.width/2, dim.height/2, 275, 125);
        this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        Container container = this.getContentPane();
        container.setLayout(new GridLayout(3, 2, 2, 2));

        container.add(labelLogin);
        container.add(inputLogin);
        container.add(labelPassword);
        container.add(inputPassword);

        buttonRegistration.addActionListener(new ButtonRegisterEventListener());
        buttonEnter.addActionListener(new ButtonEnterEventListener());
        container.add(buttonRegistration);
        container.add(buttonEnter);
    }

    static class ButtonRegisterEventListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            RegistrationWindow registrationWindow = new RegistrationWindow();
            registrationWindow.setVisible(true);
        }
    }

    class ButtonEnterEventListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (inputLogin.getText().trim().length() > 0 && inputPassword.getText().trim().length() > 0) {
                try{
                    if(inputLogin.getText().equals("admin") && inputPassword.getText().equals("admin")){
                        AdminWindow adminWindow = new AdminWindow();
                        adminWindow.setVisible(true);
                        return;
                    }
                    boolean userNum = Timetable.currentUser.enter(inputLogin.getText(), inputPassword.getText());
                    if (userNum) {
                        LoginWindow.this.dispose();
                        Window window = new Window();
                        window.setVisible(true);
                    }
                }
                catch (Exception e1){
                    JOptionPane.showMessageDialog(null, "Проверьте введённые данные.", "Error", JOptionPane.PLAIN_MESSAGE);
                }
            }
            else
                JOptionPane.showMessageDialog(null, "Поля ввода должны быть заполнены.", "Error", JOptionPane.PLAIN_MESSAGE);
        }
    }
}
