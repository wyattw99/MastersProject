package com.example.finalproject;

import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.PreferenceManager;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.VolleyError;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class GameActivity extends AppCompatActivity {
    private final static String TAG = GameActivity.class.getSimpleName();
    String word; // = "shirt";
    //ArrayList<String> randomWord = new ArrayList<>();
    ArrayList<String> wordList =new ArrayList<>();// will be updated to be a list of valid words
    ArrayList<String> wordLetters = new ArrayList<>();
    int numUserGuesses = 0;
    //private ProgressBar progressBar;
    private final WordsFetcher.OnWordsReceivedListener mFetchWordsListListener =
            new WordsFetcher.OnWordsReceivedListener() {
                @Override
                public void onWordsReceived(List<String> words) {
                    //progressBar.setVisibility(View.GONE);
                    wordList = (ArrayList<String>) words;
                }

                @Override
                public void onWordsReceived(String word) {

                }

                @Override
                public void onErrorReceived(VolleyError error) {
                    Log.d(TAG, error.toString());
                }
            };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        SharedPreferences mPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String numGuessesString = mPreferences.getString("difficulty","6");
        String numLettersString = mPreferences.getString("letters","5");
        int numGuesses = Integer.parseInt(numGuessesString);
        int numLetters = Integer.parseInt(numLettersString);
        int numTextViews = numGuesses * numLetters;
        super.onCreate(savedInstanceState);
        setContentView(GameTools.getLayout(numGuesses,numLetters));
        EditText userGuess = findViewById(R.id.guess_input);
        Button submitBtn = findViewById(R.id.submit_button);
        Button newGameBtn = findViewById(R.id.new_game_button);
        Button nextWordBtn = findViewById(R.id.next_word_button);
        nextWordBtn.setVisibility(View.GONE);
        nextWordBtn.setEnabled(false);
        TextView Title = findViewById(R.id.test_view);
        Title.setText(R.string.game_mode);
        TextView[] mTextView = new TextView[numTextViews];
        WordsFetcher wordsFetcher = new WordsFetcher(this);
        wordsFetcher.fetchWords(mFetchWordsListListener);



        word = getIntent().getStringExtra("random_word");

        for (int i = 0; i < word.length(); i++) {
            String letter;
            letter = String.valueOf(word.charAt(i));
            wordLetters.add(letter);
        }
        for (int i = 0; i < mTextView.length; i++) {
            int resId = getResources().getIdentifier("result_box_" + (i+1), "id", getPackageName());
            mTextView[i] = findViewById(resId);
        }
        newGameBtn.setOnClickListener(view -> {
            Intent restartIntent = getIntent();
            word = GameTools.getRandomWord(wordList,numLetters);
            restartIntent.putExtra("random_word",word);
            finish();
            startActivity(restartIntent);
        });

        ArrayList<String> userLetters = new ArrayList<>();
        submitBtn.setOnClickListener(view -> {
            String guess = userGuess.getText().toString();
            guess = guess.replaceAll("\\s", "");
            userGuess.setText("");
            if(GameTools.isValidGuess(word,guess,wordList)){
                numUserGuesses = numUserGuesses+1;
                for (int i = 0; i < guess.length(); i++) {
                    String letter;
                    letter = String.valueOf(guess.charAt(i));
                    userLetters.add(letter);
                }
                int checkNumber;
                int wordLetterLocation;
                String letter;
                for(int i = 0;i < userLetters.size();i++){
                    checkNumber = GameTools.findCheckNumber(i,numLetters);
                    letter = userLetters.get(i);
                    if(wordLetters.contains(letter)){
                        if(letter.equalsIgnoreCase(wordLetters.get(i-checkNumber)) && Collections.frequency(wordLetters,letter) > 1){
                            for (int a = 0; a<wordLetters.size();a++){
                                String wordLetter = wordLetters.get(a);
                                if(letter.equalsIgnoreCase(wordLetter) && (i-checkNumber == a) ){
                                    mTextView[i].setText(letter);
                                    mTextView[i].setBackgroundColor(getResources().getColor(R.color.green));
                                }
                            }
                        } else {
                            wordLetterLocation = wordLetters.indexOf(letter);
                            if((i-checkNumber) == wordLetterLocation){
                                mTextView[i].setText(letter);
                                mTextView[i].setBackgroundColor(getResources().getColor(R.color.green));
                            }else {
                                mTextView[i].setText(letter);
                                mTextView[i].setBackgroundColor(getResources().getColor(R.color.red));
                            }
                        }
                    }else{
                        mTextView[i].setText(letter);
                        mTextView[i].setBackgroundColor(getResources().getColor(R.color.grey));
                    }
                }
                if(guess.equalsIgnoreCase(word) && numUserGuesses < numGuesses){
                    Toast.makeText(GameActivity.this, "Congratulations,you win, please start a new game or return to the menu", Toast.LENGTH_LONG).show();
                    submitBtn.setEnabled(false);
                }
                if(numUserGuesses >= numGuesses && guess.equalsIgnoreCase(word)){
                    Toast.makeText(GameActivity.this, "Congratulations,you win, please start a new game or return to the menu", Toast.LENGTH_LONG).show();
                    submitBtn.setEnabled(false);
                } else if(numUserGuesses >= numGuesses){
                    Toast.makeText(GameActivity.this,"Game Over please return to menu or start new game The word was " +word,Toast.LENGTH_LONG).show();
                    submitBtn.setEnabled(false);
                }
            }else{
                Toast.makeText(GameActivity.this, "Please provide a valid guess", Toast.LENGTH_SHORT).show();
            }
        });
    }
}

