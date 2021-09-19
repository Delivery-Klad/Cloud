package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class RegistrationWindow extends JFrame {
    private JLabel labelName = new JLabel("Имя: ");
    private JLabel labelLogin = new JLabel("Логин: ");
    private JLabel labelPassword = new JLabel("Пароль: ");
    private JTextField inputName = new JTextField("");
    private JTextField inputLogin = new JTextField("");
    private JTextField inputPassword = new JTextField("");
    private JButton buttonRegistration = new JButton("Регистрация");

    RegistrationWindow() {
        super("Меню регистрации");
        Dimension dim = getToolkit().getScreenSize();
        this.setBounds(dim.width/2, dim.height/2, 275, 125);
        this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        Container container = this.getContentPane();
        container.setLayout(new GridLayout(4, 2, 2, 2));

        container.add(labelName);
        container.add(inputName);
        container.add(labelLogin);
        container.add(inputLogin);
        container.add(labelPassword);
        container.add(inputPassword);

        buttonRegistration.addActionListener(new ButtonRegisterEventListener());
        container.add(buttonRegistration);
    }

    class ButtonRegisterEventListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (inputName.getText().trim().length() > 0
                    && inputLogin.getText().trim().length() > 0
                    && inputPassword.getText().trim().length() > 0) {
                if (findUser(inputLogin.getText(), inputPassword.getText()) == null) {
                    JOptionPane.showMessageDialog(null, "Регистрация прошла успешно, " + inputName.getText() + "!", "INFO", JOptionPane.PLAIN_MESSAGE);
                    Timetable.currentUser = new Professor(inputName.getText(), inputLogin.getText(), inputPassword.getText());
                    Timetable.users.add(Timetable.currentUser);
                    RegistrationWindow.this.dispose();
                }
                else {
                    JOptionPane.showMessageDialog(null, "Пользователь уже зарегистрирован.", "Error", JOptionPane.PLAIN_MESSAGE);
                }
            }
        }
        private Professor findUser(String login, String password) {
            for (Professor i : Timetable.users) {
                if (i.getLogin().equals(login) && i.getPassword().equals(password)) {
                    return i;
                }
            }
            return null;
        }
    }
}
