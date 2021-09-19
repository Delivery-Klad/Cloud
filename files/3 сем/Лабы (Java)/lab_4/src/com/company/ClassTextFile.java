package com.company;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class ClassTextFile {
    private String file1 = "Input.txt";

    ClassTextFile(String file1) {
        try {
            if (!new File(file1).createNewFile())
                System.out.println("File already exists!");
            else
                this.file1 = file1;
        } catch (IOException ignored) {}
    }

    book setBook() throws FileNotFoundException {
        Scanner in = new Scanner(System.in);
        System.out.print("Введите автора: ");
        String author = in.nextLine();
        System.out.print("Введите название: ");
        String name = in.nextLine();
        System.out.print("Введите id: ");
        String id = in.nextLine();
        System.out.print("Введите издание: ");
        String pub = in.nextLine();
        System.out.print("Введите кол-во страниц: ");
        String count = in.nextLine();
        System.out.print("Введите цену: ");
        String cost = in.nextLine();
        return new book(author, name, id, pub, count, cost);
    }
}