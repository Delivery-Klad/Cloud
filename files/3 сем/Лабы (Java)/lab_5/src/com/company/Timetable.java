package com.company;
import java.util.ArrayList;

public class Timetable
{
    public static ArrayList<Professor> users;
    public static ArrayList<Request> requests;
    public static Pairs[][] pairs;
    public static Professor currentUser;
    public static int rooms;
    public static int groups;

    public static void main(String[] args) {
        LoginWindow loginWindow = new LoginWindow();
        loginWindow.setVisible(true);
        for (int i = 0; i < 6; ++i) {
            for (int j = 0; j < 6; ++j) {
                Timetable.pairs[i][j] = new Pairs();
            }
        }
    }
}
