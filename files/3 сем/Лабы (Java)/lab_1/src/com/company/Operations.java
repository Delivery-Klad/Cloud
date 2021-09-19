package com.company;
import java.util.Scanner;
import java.util.Random;

public class Operations {
    int count;
    Scanner in = new Scanner(System.in);
    double[] Mass;

    private void Fill(int i){
        final Random random = new Random();
        if(i == 0){
            for(int a = 0; a < count; a++){
                Mass[a] = random.nextInt(100);
            }
        }
        else if(i == 1){
            for(int a = 0; a < count; a++){
                System.out.print("Введите "+(a+1)+" элемент массива: ");
                Mass[a] = in.nextDouble();
            }
        }
        else{
            System.out.println("Некорректный ввод");
        }
    }
    private void Out(int i){
        if(i == 0){
            System.out.print("Массив слева направо: ");
            for(int a = 0; a < count; a++){
                System.out.print(Mass[a] + " ");
            }
            System.out.println(" ");
        }
        else if(i == 1){
            System.out.println("Массив справа налево: ");
            for(int a = count-1; a >= 0; a--){
                System.out.print(Mass[a] + " ");
            }
            System.out.println(" ");
        }
        else{
            System.out.println("Некорректный ввод");
        }
    }
    public double MiddleAr(){
        double Sum = 0;
        int k = 0;
        for(int i = 0; i < count; i++){
            if(i % 2 == 0){
                Sum += Mass[i];
                k++;
            }
        }
        return Sum / k;
    }
    public double MiddleGeo(){
        double Sum = 1;
        int k = 0;
        for(int i = 0; i < count; i++){
            if(i % 2 == 0){
                Sum *= Mass[i];
                k++;
            }
        }
        return Math.pow(Sum, 1.0 / k );
    }
    public void Sort(){
        int left = 1;
        int right = count - 1;
        while (left <= right)
        {
            for (int i = right; i >= left; i--)
                if (Mass[i - 1] < Mass[i]) Swap(i);
            left++;

            for (int i = left; i <= right; i++)
                if (Mass[i - 1] < Mass[i]) Swap(i);
            right--;
        }
    }
    private void Swap(int i){
        double buff;
        buff = Mass[i];
        Mass[i] = Mass[i - 1];
        Mass[i - 1] = buff;
    }
    public void menu(){
        System.out.println("Введите кол-во элементов массива: ");
        count = in.nextInt();
        Mass = new double[count];
        System.out.println("Заполнение массива:\n0-Случайно\n1-С клавиатуры");
        int random = in.nextInt();
        Fill(random);
        System.out.println("Вывод массива:\n0-Слева направо\n1-Справа налево");
        int out_mass = in.nextInt();
        Out(out_mass);
    }
}

