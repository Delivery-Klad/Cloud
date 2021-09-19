package com.company;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
class Task1 {
    private String line = "";
    private String line2 = "";
    private int x = 0;
    private String res = "";
    private ArrayList<Double> Mass = new ArrayList<>();
    void Input(String line){
        if (line.charAt(line.length() - 1) != ' ')
            line += ' ';
        res = line;
        this.line = line;
    }
    int CountAbz(){
        int count = 0;
        int temp = 0;
        for(int i = 0; i < line.length(); i++){
            if(temp != count){
                if(temp!=0) {
                    CountPhone(line2, temp);
                    Split(line2);
                }
                line2 = "";
                temp = count;
            }
            else{
                line2 += line.charAt(i);
            }
            if(line.charAt(i) == '\t')
                count +=1;
        }
        CountPhone(line2, temp);
        line = res;
        line2 = "";
        x = 0;
        return count;
    }
    private void CountPhone(String line2, int temp){
        String str = line2;
        double sum = 0.0;
        Pattern pattern = Pattern.compile("-?\\d+(\\.\\d+)?");
        Matcher matcher = pattern.matcher(str);
        while(matcher.find()) {
            sum += Double.parseDouble(matcher.group());
        }
        Mass.add(sum);
        System.out.println("Время разговоров в " + temp + " абзаце: " + sum);
    }
    private void Split(String line3) {
        if(x==0){
            System.out.println("Первый абзац, разбитый на предложения");
            for (String predl : line3.split(". ")) {
                System.out.println(predl);
            }
            x+=1;
        }
    }
}
