package com.example.voiceapps;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.os.StrictMode;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.net.InetAddress;

public class MainActivity extends AppCompatActivity{

    ImageView speachButton;
    EditText speachText;

    EditText rT;
    private static final int RECOGNIZER_RESULT = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main) ;
        speachButton = findViewById(R.id.imageView);
        speachText = findViewById(R.id.editText);
        rT = findViewById(R.id.responseTextView);
        speachButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent speachIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                speachIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                speachIntent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speach to text");
                 startActivityForResult(speachIntent, RECOGNIZER_RESULT);
            }
        });

        // 在主线程中不允许执行网络操作，因此需要设置网络操作策略
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        // 创建新线程以执行Socket通信
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // 服务器的IP地址和端口
                    String serverAddress = "192.168.1.70";
                    int serverPort = 9999;

                    // 创建Socket连接
                    Socket socket = new Socket(serverAddress, serverPort);
                    // 发送数据到服务器
                    String messageToSend = "Hello, Server!";
                    OutputStream outputStream = socket.getOutputStream();
                    outputStream.write(messageToSend.getBytes());
                    // 接收从服务器返回的数据
                    BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    final String receivedMessage = reader.readLine();

                    // 在主线程中更新UI，显示接收到的数据
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            rT.setText("服务器返回的消息: " + receivedMessage);
                        }
                    });

                    // 关闭连接
                    socket.close();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        thread.start();

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data){
        if(requestCode == RECOGNIZER_RESULT && resultCode == RESULT_OK){
            ArrayList<String> matches = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            System.out.println(0);
            try {
                InetAddress addr = InetAddress.getLocalHost();
            } catch (IOException e) {
                System.out.println(-100);
            }
            String s = matches.get(0).toString();
            speachText.setText(s);
            try {
                Socket socket = new Socket("192.168.1.70",9999);
                OutputStream op = socket.getOutputStream();
                PrintWriter pw = new PrintWriter((op));
                pw.write(s);
                pw.flush();
                pw.close();
            } catch (IOException e) {
                System.out.println(-1);
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
}