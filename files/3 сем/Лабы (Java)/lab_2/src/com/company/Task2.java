package com.company;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Task2 {
    private StringBuilder line;
    private StringBuilder line1;
    private StringBuffer line2;
    private StringBuffer line3;
    Boolean d = false;
    private ArrayList<Integer> Mass = new ArrayList<>();
    private ArrayList<Integer> Mass2 = new ArrayList<>();
    private String res = "";
    private Pattern pattern = Pattern.compile("-?\\d+(\\.\\d+)?");
    void Input(String str){
        try {
            if (str.charAt(str.length() - 1) != ' ')
                str += " ";
            line = new StringBuilder(str);
            line1 = new StringBuilder(" ");
            res = str;
            line2 = new StringBuffer(" ");
            line3 = new StringBuffer(" ");
        }
        catch(Exception e) {
            System.out.println("Error");
        }
    }
    void CountAbz(){
        try {
            int count = 0;
            int temp = 0;
            int temp2 = 0;
            int max = 0;
            String tmp = "";
            for (int i = 0; i < line.length() - 2; i++) {
                temp += 1;
                temp2 += 1;
                if (count == 1) {
                    tmp = String.valueOf(line.charAt(i));
                    line2.append(tmp);
                }
                if (line.charAt(i) == '\t') {
                    count += 1;

                    if (count != 1) {
                        Mass.add(temp);
                        Mass2.add(temp2);
                        if (temp > max)
                            max = temp;
                    }
                    temp = 0;
                }
            }
            if (temp > max)
                max = temp;
            Mass.add(temp);
            Mass2.add(temp2);
            int ind = Mass.indexOf(max);
            tmp = String.valueOf(line2);
            if (ind != 0) {
                line.delete(Mass2.get(ind - 1), Mass2.get(ind)-1);
                line.delete(0, Mass2.get(0));
                line.append("\t").append(tmp);
            } else {
                line.delete(0, Mass2.get(ind)-1);
                line.append("\t").append(tmp);
            }
            System.out.println(line);
            String str  = "";
            for (int i = 0; i < line.length(); i++) {
                if (line.charAt(i) == '\t') {
                    str = String.valueOf(line2);
                    Update(str);
                    line2.delete(0,line2.length());
                    line3.delete(0,line3.length());
                }
                line2.append(line.charAt(i));
            }
            line.delete(0,line.length());
            line.append(res);
            line2.delete(0,line2.length());
            line2.append(" ");
            System.out.print(line1+"\n");
        }
        catch(Exception ignored) {

        }
    }
    private void Update(String str){
        double t = 0;
        line3.append(str);
        Matcher matcher = pattern.matcher(str);
        String temp = "";
        while(matcher.find()) {
            t = Double.parseDouble(matcher.group());
            temp = String.valueOf(t);
            line3.replace(matcher.start(), matcher.start()+temp.length(), Modify(t));
        }
        if(d)
            line1.append(line3);
        d = true;
    }
    private String Modify(double b){
        double t = Double.parseDouble(String.valueOf(b));
        int a = 0;
        while(true){
            if(t>1){
                t/=10;
                a+=1;
            }
            else
                break;
        }
        return  t +"*exp*10^"+a;
    }
}
