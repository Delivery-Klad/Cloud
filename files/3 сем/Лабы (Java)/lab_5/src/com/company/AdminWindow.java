package com.company;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class AdminWindow extends JFrame{
    private JLabel countGroups = new JLabel("Количество групп: ");
    private JLabel countRooms = new JLabel("Количество аудиторий: ");
    private JTextField inputGroups = new JTextField("");
    private JTextField inputRooms = new JTextField("");
    private JButton buttonSet = new JButton("Установить");

    AdminWindow() {
        super("Меню администратора");
        Dimension dim = getToolkit().getScreenSize();
        this.setBounds(dim.width/2, dim.height/2, 350, 125);
        this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        Container container = this.getContentPane();
        container.setLayout(new GridLayout(3, 2, 2, 2));

        container.add(countGroups);
        container.add(inputGroups);
        container.add(countRooms);
        container.add(inputRooms);

        buttonSet.addActionListener(new ButtonRegisterEventListener());
        container.add(buttonSet);
    }

    class ButtonRegisterEventListener implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (inputGroups.getText().trim().length() > 0
                    && inputRooms.getText().trim().length() > 0){
                Timetable.groups = Integer.parseInt(inputGroups.getText());
                Timetable.rooms = Integer.parseInt(inputRooms.getText());
                processRequests();
                JOptionPane.showMessageDialog(null, "Кол-во групп и аудиторий установлено.", "INFO", JOptionPane.PLAIN_MESSAGE);

            }
            AdminWindow.this.dispose();
        }
    }
    private static void processRequests() {
        for (Request r : Timetable.requests) {
            int number = r.getPairs();
            for (int i = 0; i < 6; ++i) {
                for (int j = 0; j < 6; ++j) {
                    int room = 1;
                    if (Timetable.pairs[i][j].getRooms() < Timetable.rooms && number > 0) {
                        while (Timetable.pairs[i][j].checkRoom(room)) {
                            ++room;
                        }
                        if (!Timetable.pairs[i][j].checkGroup(r.getGroup()) && !Timetable.pairs[i][j].checkProfessor(r.getRequester())) {
                            Timetable.pairs[i][j].setPair(r.getRequester(), r.getDiscipline(), room, r.getGroup(), j, i);
                            Timetable.pairs[i][j].Group_(r.getGroup());
                            Timetable.pairs[i][j].Prof_(r.getRequester());
                            Timetable.pairs[i][j].Room_(room);
                            --number;
                        }
                    }
                }
            }
        }
    }
}
