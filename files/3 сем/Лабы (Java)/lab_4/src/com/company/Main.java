package com.company;
import java.io.File;
import java.io.*;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.io.IOException;
import java.util.Scanner;

public class Main
{
    public static void main(String[] args) {
        try{
            print("\n1.Исследовать возможности класса File по созданию файлов (пустых) и папок программой. Применение конструктора и метода");
            task1_1();
            print("\n2.Получить параметры файлов методами класса File, в пунктах задания использовать объекты, созданные в задании 1");
            task1_2();
            print("\n3.Модификация файловой структуры приложения средствами класса File");
            task1_3();

            task2();

            print("\n1.Чтение из одного файла текстового файла и запись в другой");
            task3_1();
            print("\n2.Применение буферизированных потоков для чтения и записи текстовых файлов");
            task3_2();
            print("\n3.Настройка кодировки символов для входного и выходного потоков");
            task3_3();

            print("Применение классов ObjectOutputStream и ObjectInputStream для сериализации и десериализации объектов ");
            task4();
        }
        catch (Exception e){
            print(String.valueOf(e));
        }
    }

    private static void createFile(String filepath, String name) {
        File file = new File(filepath, name);
        file.getParentFile().mkdir();
        if (!file.exists()) {
            try {
                file.createNewFile();
                print("Файл создан");
                return;
            }
            catch (IOException e) {
                print(e.getMessage());
                return;
            }
        }
        print("Файл  уже создан");
    }

    private static void createDirectory(String filepath) {
        File file = new File(filepath);
        if (!file.exists()) {
            file.mkdirs();
            print("Файл создан");
            return;
        }
        print("Файл уже создан");
    }

    private static void deleteFile(String filepath, String name) {
        File file = new File(filepath, name);
        if (file.delete()) {
            print("Файл " + file.getName() + " удален");
            return;
        }
        print("Ошибка удаления");
    }

    private static void deleteDirectory(String filepath) {
        File file = new File(filepath);
        if (file.delete()) {
            print("Папка " + file.getName() + " удалена");
            return;
        }
        print("Ошибка удаления");
    }

    private static String[] getFiles() {
        File file = new File(".");
        return file.list();
    }

    private static File[] getFolders() {
        File file = new File(".");
        return file.listFiles();
    }

    private static void foldersCount(File[] files) {
        int count = 0;
        for (File file : files) {
            if (file.isDirectory()) {
                ++count;
            }
        }
        print(String.valueOf(count));
    }

    private static void task1_1(){
        createFile(".", "MyFile1.txt");
        createFile("F:\\", "MyFile2.txt");
        createFile("C:\\Steam\\", "MyFile3.txt");
        createDirectory("Первая\\Вторая\\Третья");
    }

    private static void task1_2() {
        File file = new File("C:\\Steam\\", "MyFile4.txt");
        File file1 = new File("MyFile1.txt");
        String exist = "";
        if (file1.exists()) {
            exist = "Файл MyFile1.txt существует";
        }
        print("Существует ли файл MyFile1.txt: " + exist + "\nИмя файла: " + file.getName() + "\nПуть к файлу: " +
                file.getAbsolutePath() + "\nВес: " + file.length() + " bytes\nТип файла: " + (file.isDirectory() ? "Папка" : "Файл"));
    }

    private static void task1_3(){
        createDirectory("one_more_folder");
        print(Arrays.toString(getFiles()));
        File[] files = getFolders();
        print(Arrays.toString(files));
        foldersCount(files);
        deleteFile(".", "MyFile1.txt");
        deleteFile("F:\\", "MyFile2.txt");
        deleteFile("C:\\Steam\\", "MyFile3.txt");
        deleteDirectory("Первая\\Вторая\\Третья");
        deleteDirectory("Первая\\Вторая");
        deleteDirectory("Первая");
        deleteDirectory("one_more_folder");
    }

    private static void task2() throws IOException {
        Scanner in = new Scanner(System.in);
        String StringBuf = "";
        print("Введите название файла: ");
        StringBuf = in.nextLine();
        StringBuf.trim();

        print("Введите кол-во книг: ");
        int IntBuf = in.nextInt();

        FileManager F = new FileManager(StringBuf);

        if(F.exist()){
            print("Файл существует");
        }else {
            print("Файл не существует и будет создан.");
            try {
                F.create();
            } catch (Exception ignored) {}
        }
        for(int i = 0; i < IntBuf; ++i){
            print("Вы вводите книгу №" + (i + 1));
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

            book Book = new book(author,name,id,pub,count,cost);
            try {
                F.write(Book);
                ArrayList<book> Books = F.GetBooks();
                print("Введите автора для поиска книги: ");
                author = in.nextLine();
                print("Введите название для поиска книги: ");
                name = in.nextLine();
                print(F.findId(author, name));
                print("Введите издание для изменения: ");
                pub = in.nextLine();
                F.changePublisher(pub);
                print("Введите автора для поиска всех книг: ");
                author = in.nextLine();
                F.oneAuthor(author);
            }
            catch (IOException ignored){}
        }
    }

    private static void task3_1(){
        try {
            Reader reader = new InputStreamReader(new FileInputStream("T1.txt"));
            Writer writer = new OutputStreamWriter(new FileOutputStream("T2.txt"));
            int x;
            while((x = reader.read()) != -1) {
                writer.write((char)x);
            }
            reader.close();
            writer.close();
            print("Перепись файлов завершена");
        }
        catch (Exception e){
            print(String.valueOf(e));
        }
    }

    private static void task3_2(){
        try {
            Writer writer = new OutputStreamWriter(new FileOutputStream("A.txt"));
            for (int i = 40; i < 552; i++) {
                writer.write((char) i);
            }
            writer.close();

            BufferedReader inb = new BufferedReader(new InputStreamReader(new FileInputStream("A.txt")), 128);
            BufferedWriter outb = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("B.txt")), 128);
            char[] buf = new char[128];
            for(int i = 0; i < 4; i++){
                inb.read(buf);
                outb.write(buf);
                outb.newLine();
            }
            inb.close();
            outb.close();
            print("Данные переписаны");
        }
        catch (Exception e){
            print(String.valueOf(e));
        }
    }

    private static void task3_3(){
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream("A.txt"), "Cp1251"));
            print(Charset.defaultCharset().name());
            String str = in.readLine();
            print(str);
            in = new BufferedReader(new InputStreamReader(new FileInputStream("B.txt"), "UTF-8"));
            str = in.readLine();
            print(str);
        }
        catch (Exception e){
            print(String.valueOf(e));
        }
    }

    private static void task4(){
        try {
            String file1path = "C:\\Users\\dakfa\\Desktop\\st\\Java\\lab4_2\\Serialization.bin";
            File fileS = new File(file1path);
            fileS.createNewFile();
            ClassTextFile input = new ClassTextFile("Input.txt");
            book fst = input.setBook();
            System.out.println("Информация о книге: "+fst.getAuthor()+" "+fst.getName()+" "+fst.getNumber()
                    +" "+fst.getPublisher()+" "+fst.getCount()+" "+fst.getCost());
            Serialization scnd = new Serialization("C:\\Users\\dakfa\\Desktop\\st\\Java\\lab4_2\\Serialization.bin");
            scnd.outBook();
            scnd.inpBook();
            Serialization trd = new Serialization("C:\\Users\\dakfa\\Desktop\\st\\Java\\lab4_2\\Serialization.bin");
            trd.addToColl();
            print("Коллекция после добавления объектов:");
            trd.printColl();
            print("Коллекция после записи/чтения:");
            trd.outColl();
            trd.inpColl();
            trd.printColl();
        } catch (IOException ignored) {}
    }

    private static void print(String txt){
        System.out.println(txt);
    }
}
