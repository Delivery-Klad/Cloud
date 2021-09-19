package com.company;

class Request {
    private Professor requester;
    private String discipline;
    private int group;
    private int pairsInWeek;

    Request(Professor requester, String disc, int group, int hours) {
        this.requester = requester;
        this.discipline = disc;
        this.group = group;
        this.pairsInWeek = hours;
    }

    String getRequester() {
        return this.requester.getName();
    }

    String getDiscipline() {
        return this.discipline;
    }

    int getGroup() {
        return this.group;
    }

    int getPairs() {
        return this.pairsInWeek;
    }
}
