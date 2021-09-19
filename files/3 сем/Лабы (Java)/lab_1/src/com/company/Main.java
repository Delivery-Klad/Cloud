package com.company;

public class Main {
    public static void main(String[] args) {
        Operations Op = new Operations();
	Op.menu();
        System.out.println("Срееднее арифметическое чисел с нечетными индексами: " + Op.MiddleAr());
        System.out.println("Срееднее геометрическое чисел с нечетными индексами: " + Op.MiddleGeo());
        System.out.print("Отсортированный массив: ");
        Op.Sort();
        for(int a = 0; a < Op.count; a++){
            System.out.print(Op.Mass[a] + " ");
        }
    }
}
