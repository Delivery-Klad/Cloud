package com.company;

class User {
    private String name;
    private String login;
    private String password;

    User(String name, String login, String password) {
        this.name = name;
        this.login = login;
        this.password = password;
    }

    boolean enter(String login, String password) {
        return this.login.equals(login) && this.password.equals(password);
    }

    String getName() {
        return this.name;
    }

    String getLogin() {
        return this.login;
    }

    String getPassword() {
        return this.password;
    }
}