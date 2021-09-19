package com.company;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class Window extends JFrame {
    private JLabel labelDict = new JLabel("Дисциплина: ");
    private JLabel labelGroup = new JLabel("Группа: ");
    private JLabel labelCount = new JLabel("Кол-во пар: ");
    private JTextField inputDict = new JTextField("");
    private JTextField inputGroup = new JTextField("");
    private JTextField inputCount = new JTextField("");
    private JButton Rec = new JButton("Сделать запрос");
    private JButton Pairs = new JButton("Узнать расписание");
    private JButton Menu = new JButton("Главное меню");
    Window() {
        super("Основное меню");
        Dimension dim = getToolkit().getScreenSize();
        this.setBounds(dim.width/2, dim.height/2, 500, 300);
        this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        Container container = this.getContentPane();
        container.setLayout(new GridLayout(7, 7, 7, 7));
        container.add(labelDict);
        container.add(inputDict);
        container.add(labelGroup);
        container.add(inputGroup);
        container.add(labelCount);
        container.add(inputCount);
        ButtonGroup group = new ButtonGroup();
        group.add(Rec);
        group.add(Pairs);
        Rec.addActionListener(new ButtonRecListener());
        container.add(Rec);

        Pairs.addActionListener(new ButtonPairsListener());
        container.add(Pairs);

        Menu.addActionListener(new ButtonMenuListener());
        container.add(Menu);
    }

    class ButtonMenuListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            Window.this.dispose();
            LoginWindow loginWindow = new LoginWindow();
            loginWindow.setVisible(true);
        }
    }

    class ButtonPairsListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            printPairs(Timetable.currentUser);
        }
    }

    class ButtonRecListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (inputDict.getText().trim().length() > 0
                    && inputGroup.getText().trim().length() > 0
                    && inputCount.getText().trim().length() > 0) {
                addRequest(inputDict.getText(), Integer.parseInt(inputGroup.getText()), Integer.parseInt(inputCount.getText()));
                JOptionPane.showMessageDialog(null, "Запрос сделан.", "ШТАЩ", JOptionPane.PLAIN_MESSAGE);
            }
            else
                JOptionPane.showMessageDialog(null, "Поля ввода должны быть заполнены.", "Error", JOptionPane.PLAIN_MESSAGE);
        }
    }

    private void printPairs(Professor user) {
        for (int i = 0; i < 6; ++i) {
            for (int j = 0; j < 6; ++j) {
                Timetable.pairs[i][j].printPair(user.getName());
            }
        }
    }

    private void addRequest(String disc, int group, int pairs) {
        Request r = new Request(Timetable.currentUser, disc, group, pairs);
        Timetable.requests.add(r);
    }
}
