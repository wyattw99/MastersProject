package com.example.finalproject;

import android.content.Context;
import android.net.Uri;
import android.util.Log;


import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;

import java.util.ArrayList;
import java.util.List;

public class WordsFetcher {
    public interface OnWordsReceivedListener {
        void onWordsReceived(List<String> words);
        void onWordsReceived(String word);
        void onErrorReceived(VolleyError error);

    }

    private final String WORDS_LIST_URL = "https://random-word-api.herokuapp.com/all";
    private final String RANDOM_WORD_URL = "https://random-word-api.herokuapp.com/word";
    private final String TAG = WordsFetcher.class.getSimpleName();
    private final RequestQueue mRequestQueue;


    public WordsFetcher(Context context) {
        mRequestQueue = Volley.newRequestQueue(context);
    }

    public void fetchWords(final OnWordsReceivedListener listener) {
        String url = Uri.parse(WORDS_LIST_URL).buildUpon()
                .build().toString();
        Log.d(TAG, url.toString());

        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, url.toString(), null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            Thread.sleep(1000);
                        } catch (Exception ex) {
                            Log.d(TAG, "error");
                        }
                        List<String> words = parseJsonWords(response);
                        listener.onWordsReceived(words);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        listener.onErrorReceived(error);
                    }
                });
        mRequestQueue.add(request);
    }
    public void fetchRandomWord(final OnWordsReceivedListener listener, String length) {
        String url = Uri.parse(RANDOM_WORD_URL).buildUpon()
                .appendQueryParameter("length",length)
                .build().toString();
        Log.d(TAG, url.toString()+" random");

        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, url.toString(), null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            Thread.sleep(5000);
                        } catch (Exception ex) {
                            Log.d(TAG, "error");
                        }
                        String word = parseJsonRandomWord(response);
                        listener.onWordsReceived(word);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        listener.onErrorReceived(error);
                    }
                });
        mRequestQueue.add(request);
    }


    List<String> parseJsonWords(JSONArray jsonArray) {
        String word;
        ArrayList<String> wordList = new ArrayList<>();
        try {
            for (int i = 0; i < jsonArray.length(); i++) {
                word = jsonArray.get(i).toString();
                wordList.add(word);
            }
        } catch (Exception e) {
            Log.d(TAG, "error");
        }
        return wordList;
    }

    String parseJsonRandomWord(JSONArray jsonArray){
        String word = null;
        ArrayList<String> words = new ArrayList<>();
        try{
            for (int i = 0; i<jsonArray.length(); i++){
                word = jsonArray.get(i).toString();
                words.add(word);
            }

        } catch (Exception e){
            Log.d(TAG,"error");
        }
        word = words.get(0);
        return word;
    }
}

