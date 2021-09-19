package com.company;
import java.util.ArrayList;

class Pairs
{
    private String[] days;
    private ArrayList<Integer> room;
    private ArrayList<Integer> group;
    private ArrayList<String> professor;
    private ArrayList<String> pair;
    Pairs() {
        this.days = new String[] { "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота" };
        this.room = new ArrayList<Integer>();
        this.group = new ArrayList<Integer>();
        this.professor = new ArrayList<String>();
        this.pair = new ArrayList<String>();
    }

    void Room_(int room) {
        this.room.add(room);
    }

    void Group_(int group) {
        this.group.add(group);
    }

    void Prof_(String professor) {
        this.professor.add(professor);
    }

    boolean checkRoom(int room) {
        return this.room.contains(room);
    }

    boolean checkGroup(int group) {
        return this.group.contains(group);
    }

    boolean checkProfessor(String professor) {
        return this.professor.contains(professor);
    }

    int getRooms() {
        return this.room.size();
    }

    void setPair(String professor, String disc, int room, int group, int hour, int day) {
        this.pair.add("группа: " + group + ", профессор: " + professor + ", дисциплина: " + disc + ", аудитория: " +
                room + ", пара:" + (hour + 1) + ", день: " + this.days[day]);
    }

    void printPair(String prof) {
        for (String i : this.pair) {
            if (i.contains(prof)) {
                System.out.println(i);
            }
        }
    }
}
