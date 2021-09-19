package com.company;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Task3 {
    private String line = "";
    void Input(String line){
        if (line.charAt(line.length() - 1) != ' ')
            line += ' ';
        this.line = line;
    }
    boolean IPv4() {
        if (line == null || line.isEmpty())
            return false;
        line = line.trim();
        if ((line.length() < 6) || (line.length() > 15))
            return false;
        try {
            Pattern pattern = Pattern.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
            Matcher matcher = pattern.matcher(line);
            return matcher.matches();
        } catch (Exception ex) {
            return false;
        }
    }
    void IPv6(){
        String str="";
        line = line.trim();
        try {
            Pattern pattern = Pattern.compile("([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}");
            Matcher matcher = pattern.matcher(line);
            while(matcher.find()) {
                str = matcher.group();
                System.out.print("IPv6: "+ str +" в двоичном представлении: ");
                Translation(str);
            }
        }
        catch (Exception ex) {
            System.out.println("error");
        }
    }
    private void Translation(String str){
        String str2="",str3="";
        int ind = 0, num = 0;
        for(int i = 0; i < 8; i++){
            str3+=":";
            for(int j = 0;j < 4;j++){
                str2 += str.charAt(ind);
                ind+=1;
            }
            num = Integer.parseInt(str2, 16);
            str3 += Integer.toBinaryString(num);
            ind+=1;
            str2 = "";
        }
        System.out.println(str3);
    }
}
