package com.company;
import java.io.*;
import java.io.File;
import java.util.ArrayList;

class FileManager {
    private String Name;
    private File file;

    public FileManager(String Name) throws IOException {
        this.Name = Name;
        file = new File(this.Name);
    }

    public void create()throws IOException {
        file.createNewFile();
    }

    public boolean exist(){
        return file.canRead();
    }

    public void write(book book) throws IOException{
        if(exist()){
            String res = "";
            DataInputStream InpStream = new DataInputStream(new FileInputStream(file.getAbsolutePath()));
            try{
                res = InpStream.readUTF();
            }
            catch (Exception ignored){}
            res = stringBook(book) + "\n" + res;
            InpStream.close();

            DataOutputStream OutStream = new DataOutputStream(new FileOutputStream(file.getAbsolutePath()));
            OutStream.writeUTF(res);
            OutStream.flush();
            OutStream.close();
        }
        else{
            throw new IOException("Файла не существует");
        }
    }

    private String read() throws IOException{
        String res = "";
        byte ress[];

        if(exist()){
            DataInputStream InpStream = new DataInputStream(new FileInputStream(file.getAbsolutePath()));
            res = InpStream.readUTF();
            System.out.println();
            InpStream.close();
        }
        return res;
    }

    public String stringBook(book book){
        String res = "";
        res += book.getAuthor() + ":" + book.getName() + ":" + book.getNumber() + ":" + book.getPublisher() + ":" + book.getCount() + ":" + book.getCost();
        return res;
    }

    public ArrayList<book> GetBooks() throws IOException{
        ArrayList<book> ArrBooks = new ArrayList<>();
        String[] books = read().split("\n");
        for (String book : books) {
            //ArrBooks.add(new book(Book));
        }
        return ArrBooks;
    }
    public ArrayList<book> oneAuthor(String author) throws IOException{
        ArrayList<book> Books = GetBooks();
        ArrayList<book> resBooks = new ArrayList<>();

        for (com.company.book book : Books) {
            if ((book.getAuthor().compareTo(author) == 0)) {
                resBooks.add(book);
            }
        }
        return resBooks;
    }
    public String findId(String author, String name) throws IOException{
        String res = "";
        String Books = randomAccess();
        String[] ArrBooks = Books.split("\n");

        for (String arrBook : ArrBooks) {
            String[] books = arrBook.split(":");
            if (books[0].compareTo(author) == 0 && books[1].compareTo(name) == 0) {
                return "Инвентарный номер: " + books[2];
            }
        }
        return res;
    }
    private String randomAccess() throws IOException{
        String nameFile = "RandomAccess.txt";
        RandomAccessFile randomFile = new RandomAccessFile(nameFile, "r");
        String res = "";
        try {
            randomFile.seek(0);
            String buff;
            while ((buff = randomFile.readLine()) != null){
                res += buff;
            }
        }
        catch (EOFException ignored){}
        return res;
    }
    public void changePublisher(String publisher) throws IOException{
        String Books = randomAccess();
        String[] ArrBooks = Books.split("\n");

        for (String arrBook : ArrBooks) {
            String[] books = arrBook.split(":");
            if (books[3].compareTo(publisher) == 0) {
                //ArrBooks.setPublisher(publisher);
            }
        }
    }
}
