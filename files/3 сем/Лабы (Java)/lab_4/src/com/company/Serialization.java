package com.company;
import java.io.*;
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

class Serialization {
    String file_1 = "C:\\Users\\dakfa\\Desktop\\st\\Java\\lab4_2\\Serialization.bin";
    String file_2 = "C:\\Users\\dakfa\\Desktop\\st\\Java\\lab4_2\\SerializationColl.bin";
    private ArrayList<book> Books = new ArrayList<book>();

    Serialization(String file_1) throws IOException {
        try {
            if (!new File(file_1).createNewFile()) {
                System.out.println("Файл существует!");
            } else {
                this.file_1 = file_1;
            }
        } catch(IOException e) {}
    }
    public void outBook() throws IOException {
        Scanner in = new Scanner(System.in);
        print("Введите автора: ");
        String author = in.nextLine();
        print("Введите название: ");
        String name = in.nextLine();
        print("Введите id: ");
        String id = in.nextLine();
        print("Введите издание: ");
        String pub = in.nextLine();
        print("Введите кол-во страниц: ");
        String count = in.nextLine();
        print("Введите цену: ");
        String cost = in.nextLine();
        book Book = new book(author, name, id, pub, count, cost);
        Book.setAuthor(author);
        Book.setName(name);
        Book.setNumber(id);
        Book.setPublisher(pub);
        Book.setCount(count);
        Book.setCost(cost);

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(file_1));
        out.writeUTF(Book.getAuthor());
        out.writeUTF(Book.getName());
        out.writeUTF(Book.getNumber());
        out.writeUTF(Book.getPublisher());
        out.writeUTF(Book.getCount());
        out.writeUTF(Book.getCost());

        out.close();
    }
    void inpBook () throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(file_1));

        book input = new book(in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF());

        System.out.println("Информация о книге: "+input.getAuthor()+" "+input.getName()+" "+input.getNumber()
                +" "+input.getPublisher()+" "+input.getCount()+" "+input.getCost());
        in.close();
    }
    public void addToColl() {
        Scanner in = new Scanner(System.in);
        print("Кол-во книг: ");
        int count = in.nextInt();
        for (int i = 0; i < count; i++) {
            print("Введите автора: ");
            String author = in.nextLine();
            print("Введите название: ");
            String name = in.nextLine();
            print("Введите id: ");
            String id = in.nextLine();
            print("Введите издание: ");
            String pub = in.nextLine();
            print("Введите кол-во страниц: ");
            String coun = in.nextLine();
            print("Введите цену: ");
            String cost = in.nextLine();
            book bk = new book(author, name, id, pub, coun, cost);
            bk.setAuthor(author);
            bk.setName(name);
            bk.setNumber(id);
            bk.setPublisher(pub);
            bk.setCount(coun);
            bk.setCost(cost);
            Books.add(bk);
        }
    }
    public void outColl() throws IOException {
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(file_2));
        for (book bk: Books) {
            out.writeUTF(bk.getAuthor());
            out.writeUTF(bk.getName());
            out.writeUTF(bk.getNumber());
            out.writeUTF(bk.getPublisher());
            out.writeUTF(bk.getCount());
            out.writeUTF(bk.getCost());
        }

        out.close();
    }

    void inpColl() throws IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(file_2));

        Books.clear();
        while(true) {
            try {
                Books.add(new book(in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF(), in.readUTF()));
            } catch (EOFException e) {
                in.close();
                break;
            }
        }
    }

    void printColl() {
        for (book bk : Books) {
            System.out.println(bk.getAuthor()+" "+bk.getName()+" "+bk.getNumber()
                    +" "+bk.getPublisher()+" "+bk.getCount()+" "+bk.getCost());
        }
    }

    ArrayList<book> getColl() {
        return Books;
    }
    private static void print(String txt){
        System.out.println(txt);
    } 
}
