package com.example.finalproject;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.PreferenceManager;


import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.VolleyError;
import com.google.android.gms.games.PlayGames;
import com.google.android.gms.tasks.OnSuccessListener;

import java.util.List;

public class MainActivity extends AppCompatActivity{
    String word;
    private final static String TAG = MainActivity.class.getSimpleName();
    int survivalScore;
    int timeScore;
    private final WordsFetcher.OnWordsReceivedListener mFetchRandomWordListener =
            new WordsFetcher.OnWordsReceivedListener() {
                @Override
                public void onWordsReceived(List<String> words) {

                }

                @Override
                public void onWordsReceived(String randomWord) {
                    word = randomWord;
                }

                @Override
                public void onErrorReceived(VolleyError error) {
                    Log.d(TAG,error.toString());
                }
            };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        SharedPreferences mSharedPreferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String numLettersString = mSharedPreferences.getString("letters","5");
        survivalScore = mSharedPreferences.getInt("survival_score",0);
        timeScore = mSharedPreferences.getInt("time_score",0);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView scoreView = findViewById(R.id.score_window);

        WordsFetcher wordsFetcher = new WordsFetcher(this);
        wordsFetcher.fetchRandomWord(mFetchRandomWordListener,numLettersString);

        Button gameBtn = findViewById(R.id.game_button);
        gameBtn.setOnClickListener(view -> {
            Intent gameIntent = new Intent(getApplicationContext(),GameActivity.class);
            gameIntent.putExtra("random_word",word);
            startActivity(gameIntent);
        });

        Button survivalModeBtn = findViewById(R.id.survival_mode_button);
        survivalModeBtn.setOnClickListener(view -> {
            Intent survivalIntent = new Intent(getApplicationContext(),SurvivalActivity.class);
            survivalIntent.putExtra("random_word",word);
            startActivity(survivalIntent);
        });

        Button timeModeBtn = findViewById(R.id.time_mode_button);
        timeModeBtn.setOnClickListener(view -> {
            Intent timeIntent = new Intent(getApplicationContext(),TimeActivity.class);
            timeIntent.putExtra("random_word",word);
            startActivity(timeIntent);
        });

        Button survivalLeaderboardBtn = findViewById(R.id.survival_leaderboard_button);
        survivalLeaderboardBtn.setOnClickListener(view -> showSurvivalLeaderBoard());

        Button timeLeaderboardBtn = findViewById(R.id.time_leaderboard_button);
        timeLeaderboardBtn.setOnClickListener(view -> showTimeLeaderBoard());

        scoreView.setText(getResources().getString(R.string.score_view_string,survivalScore,timeScore));
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.options_menu,menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            Intent startSettingsActivity = new Intent(this, SettingsActivity.class);
            startActivity(startSettingsActivity);
        }
        return super.onOptionsItemSelected(item);
    }

    private static final int LEADERBOARD_UI = 1119;
    private void showSurvivalLeaderBoard() {
        PlayGames.getLeaderboardsClient(this)
                .getLeaderboardIntent(getString(R.string.leaderboard_survival_mode))
                .addOnSuccessListener(new OnSuccessListener<Intent>() {
                    @Override
                    public void onSuccess(Intent intent) {
                        startActivityForResult(intent,LEADERBOARD_UI);
                    }
                });
    }
    private void showTimeLeaderBoard(){
        PlayGames.getLeaderboardsClient(this)
                .getLeaderboardIntent(getString(R.string.leaderboard_time_mode))
                .addOnSuccessListener(new OnSuccessListener<Intent>() {
                    @Override
                    public void onSuccess(Intent intent) {
                        startActivityForResult(intent,LEADERBOARD_UI);
                    }
                });
    }
}