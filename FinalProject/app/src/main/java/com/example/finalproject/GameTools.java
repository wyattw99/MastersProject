package com.example.finalproject;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Random;

public class GameTools extends AppCompatActivity {
    public static boolean isWord(ArrayList<String> wordList, String userGuess){
        return wordList.contains(userGuess);
        //return true; //for now will always be true for testing purpose
    }
    public static boolean isValidGuess(String word, String userGuess, ArrayList<String> wordList){
        if(userGuess.length() == word.length()){
            return isWord(wordList, userGuess);
        } else {
            return false;
        }
    }
    public static int findCheckNumber(int i,int numLetters){
        if (i<=(numLetters-1)){
            return 0;
        }else if(i<=(2*numLetters-1)){
            return numLetters;
        }else if(i<=(3*numLetters-1)){
            return 2*numLetters;
        }else if(i<=(4*numLetters-1)){
            return 3*numLetters;
        }else if(i<=(5*numLetters-1)){
            return 4*numLetters;
        }else if(i<=(6*numLetters-1)){
            return 5*numLetters;
        }else if(i<=(7*numLetters-1)){
            return 6*numLetters;
        }else if(i<=(8*numLetters-1)){
            return 7*numLetters;
        }else if(i<=(9*numLetters-1)){
            return 8*numLetters;
        }else{
            return 9*numLetters;
        }
    }
    public static String getRandomWord(ArrayList<String> words, int numLetters){
        ArrayList<String> possibleWords = new ArrayList<>();
        int numWords;
        String word;
        Random random = new Random();
        for (int i = 0;  i<words.size(); i++){
            if (words.get(i).length() == numLetters){
                possibleWords.add(words.get(i));
            }
        }
        numWords = possibleWords.size();
        word = possibleWords.get(random.nextInt(numWords));
        return word;
    }
    public static int getLayout(int numGuesses, int numLetters){
        int layoutResID;
        if(numLetters == 3){
            if(numGuesses == 3){
                layoutResID = R.layout.three_guesses_three;
            } else if(numGuesses == 6){
                layoutResID = R.layout.six_guesses_three;
            } else if(numGuesses == 8){
                layoutResID = R.layout.eight_guesses_three;
            } else{
                layoutResID = R.layout.ten_guesses_three;
            }
        } else if(numLetters == 4){
            if(numGuesses == 3){
                layoutResID = R.layout.three_guesses_four;
            } else if(numGuesses == 6){
                layoutResID = R.layout.six_guesses_four;
            } else if(numGuesses == 8){
                layoutResID = R.layout.eight_guesses_four;
            } else{
                layoutResID = R.layout.ten_guesses_four;
            }
        } else if(numLetters == 5) {
            if (numGuesses == 3) {
                layoutResID = R.layout.three_guesses_five;
            } else if (numGuesses == 6) {
                layoutResID = R.layout.six_guesses_five;
            } else if (numGuesses == 8) {
                layoutResID = R.layout.eight_guesses_five;
            } else {
                layoutResID = R.layout.ten_guesses_five;
            }
        } else if(numLetters == 6) {
            if (numGuesses == 3) {
                layoutResID = R.layout.three_guesses_six;
            } else if (numGuesses == 6) {
                layoutResID = R.layout.six_guesses_six;
            } else if (numGuesses == 8) {
                layoutResID = R.layout.eight_guesses_six;
            } else {
                layoutResID = R.layout.ten_guesses_six;
            }
        } else if(numLetters == 7) {
            if (numGuesses == 3) {
                layoutResID = R.layout.three_guesses_seven;
            } else if (numGuesses == 6) {
                layoutResID = R.layout.six_guesses_seven;
            } else if (numGuesses == 8) {
                layoutResID = R.layout.eight_guesses_seven;
            } else {
                layoutResID = R.layout.ten_guesses_seven;
            }
        } else{
            if (numGuesses == 3) {
                layoutResID = R.layout.three_guesses_eight;
            } else if (numGuesses == 6) {
                layoutResID = R.layout.six_guesses_eight;
            } else if (numGuesses == 8) {
                layoutResID = R.layout.eight_guesses_eight;
            } else {
                layoutResID = R.layout.ten_guesses_eight;
            }
        }

        return layoutResID;
    }
}
