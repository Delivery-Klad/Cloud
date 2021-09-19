package com.company;
import java.util.Scanner;
public class Main {

    public static void main(String[] args) {
        int menu = 100;
        Scanner in = new Scanner(System.in);
        try {
            while (menu != 0) {
                System.out.print("[0] - Завершение работы" + '\n' + "[1] - Задание 1" + '\n' +
                        "[2] - Задание 2" + '\n' + "[3] - Задание 3" + '\n' + "Выберите задание: ");
                menu = in.nextInt();
                switch (menu) {
                    case 0:
                        System.out.print("Работа завершена");
                        break;
                    case 1:
                        task1(in);
                        break;
                    case 2:
                        task2(in);
                        break;
                    case 3:
                        task3(in);
                        break;
                }
            }
        } catch(Exception ignored){

        }
    }
    private static void task1(Scanner in){
        Task1 obj = new Task1();
        int menu = 100;
        try {
            while (menu != 0) {
                System.out.print("[0] - Главное меню" + '\n' + "[1] - Ввести текст" + '\n' +
                        "[2] - Узнать количество абзацев, время разговора в каждом абзаце и разделить первый абзац" + '\n' +
                        "Выберете задание: ");
                menu = in.nextInt();
                switch (menu) {
                    case 0:
                        System.out.println("Возвращение в главное меню...");
                        break;
                    case 1:
                        System.out.println("Введите текст: ");
                        in.nextLine();
                        String str = in.nextLine();
                        obj.Input(str);
                        break;
                    case 2:
                        System.out.println("Абзацев: " + obj.CountAbz());
                        break;
                }
            }
        } catch(Exception ignored){

        }
    }
    private static void task2(Scanner in){
        Task2 obj = new Task2();
        int menu = 100;
        try {
            while (menu != 0) {
                System.out.print("[0] - Главное меню" + '\n' + "[1] - Ввести текст" + '\n' +
                        "[2] - Удалить самый длинный абзац, представить числа в форме с плавающей точкой и выполнить модификацию текста" + '\n' +
                        "Выберете задание: ");
                menu = in.nextInt();
                switch (menu) {
                    case 0:
                        System.out.println("Возвращение в главное меню...");
                        break;
                    case 1:
                        System.out.println("Введите текст: ");
                        in.nextLine();
                        String str = in.nextLine();
                        obj.Input(str);
                        break;
                    case 2:
                        obj.CountAbz();
                        break;
                }
            }
        } catch(Exception ignored){

        }
    }
    private static void task3(Scanner in){
        Task3 obj = new Task3();
        int menu = 100;
        try {
            while (menu != 0) {
                System.out.print("[0] - Главное меню" + '\n' + "[1] - Ввести текст" + '\n' +
                        "[2] - Поверить соответствие строки формату IP-адреса v4" + '\n' +
                        "[3] - Второе задание" + '\n' +
                        "Выберете задание: ");
                menu = in.nextInt();
                switch (menu) {
                    case 0:
                        System.out.println("Возвращение в главное меню...");
                        break;
                    case 1:
                        System.out.println("Введите текст: ");
                        in.nextLine();
                        String str = in.nextLine();
                        obj.Input(str);
                        break;
                    case 2:
                        if(obj.IPv4())
                            System.out.println("IP соответствует формату IPv4\n");
                        else
                            System.out.println("IP не соответствует формату IPv4\n");
                        break;
                    case 3:
                        obj.IPv6();
                        break;
                }
            }
        } catch(Exception ignored){

        }
    }
}
