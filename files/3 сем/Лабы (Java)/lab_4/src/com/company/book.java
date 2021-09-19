package com.company;

public class book {
    private String Author;
    private String Name;
    private String Number;
    private String Publisher;
    private String Count;
    private String Cost;

    public book(String author,  String name, String number, String publisher, String count, String cost){
        setAuthor(author);
        setName(name);
        setNumber(number);
        setPublisher(publisher);
        setCount(count);
        setCost(cost);
    }

    public String getAuthor() {  return Author; }
    public String getName() {   return Name; }
    public String getNumber() {   return Number; }
    public String getPublisher() {    return Publisher; }
    public String getCount() {  return Count; }
    public String getCost() {   return Cost; }

    public void setAuthor(String author) { this.Author = author; }
    public void setName(String name) {   this.Name = name; }
    public void setNumber(String number) {   this.Number = number; }
    public void setPublisher(String publisher) {    this.Publisher = publisher; }
    public void setCount(String count) {  this.Count = count; }
    public void setCost(String cost) {   this.Cost = cost; }

    private String getNumber(String name, String author){
        return Number;
    }

    private String checkBooks(){
        if(true)
            return "Книги изданы в 1 издании";
        else
            return "Книги не изданы в 1 издании";
    }

    private void authorBooks(String author){
        print(" ");
    }

    private void changePublisher(String pub1, String pub2){
        print("");
    }

    private void print(String txt){
        System.out.println(txt);
    }
}

