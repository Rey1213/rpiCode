package com.reynaldojr.raspberryconnect;

import android.os.Message;

import java.io.BufferedReader; //Lee texto de un Stream
import java.io.IOException; //Excepciones de Input/Output
import java.io.InputStream; //Para Input Stream de Bytes
import java.io.InputStreamReader; //Byte Stream -> Character Stream
import java.io.OutputStream;    //Output Stream de Bytes
import java.io.PrintWriter; //Imprime a Text Output Stream
import java.net.Socket; //Para Socket (destino para comunicacion entre 2 maquinas)

public class ClientThread extends Thread{

    String dstAddress;
    int dstPort;
    private boolean running;
    MainActivity.ClientHandler handler;

    Socket socket;
    PrintWriter printWriter;
    BufferedReader bufferedReader;

    public ClientThread(String addr, int port, MainActivity.ClientHandler handler) {
        super();
        dstAddress = addr;
        dstPort = port;
        this.handler = handler;
    }

    public void setRunning(boolean running){
        this.running = running;
    }

    private void sendState(String state){
        handler.sendMessage(
                Message.obtain(handler,
                        MainActivity.ClientHandler.UPDATE_STATE, state));
    }

    public void txMsg(String msgToSend){
        if(printWriter != null){
            printWriter.println(msgToSend);
        }
    }

    @Override
    public void run() {
        sendState("conectando...");

        running = true;

        try {
            socket = new Socket(dstAddress, dstPort); //Direccion y Puerto donde se conecta
            sendState("Conectado");

            OutputStream outputStream = socket.getOutputStream();   //Lo que sale del dispositivo
            printWriter = new PrintWriter(outputStream, true);

            InputStream inputStream = socket.getInputStream();  //Lo que entra al dispositivo
            InputStreamReader inputStreamReader =
                    new InputStreamReader(inputStream);
            bufferedReader = new BufferedReader(inputStreamReader);

            while(running){

                
                String line = bufferedReader.readLine();    //Leer linea
                if(line != null){
                    handler.sendMessage(            //Mandar mensaje
                            Message.obtain(handler,
                                    MainActivity.ClientHandler.UPDATE_MSG, line));
                }

            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if(bufferedReader != null){
                try {
                    bufferedReader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            if(printWriter != null){
                printWriter.close();
            }

            if(socket != null){
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        handler.sendEmptyMessage(MainActivity.ClientHandler.UPDATE_END);
    }
}
