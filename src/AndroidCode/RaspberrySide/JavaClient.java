import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class JavaClient {

    public static void main(String[] args) {
        System.out.println("Run Client");
        System.out.println("Runtime Java: " 
                + System.getProperty("java.runtime.version"));
        
        if(args.length != 2){
            System.out.println("usage: java client <port> <something>");
            System.exit(1);
        }
        
        int port = isParseInt(args[0]);
        if(port == -1){
            System.out.println("usage: java client <port> <something>");
            System.out.println("<port>: integer");
            System.exit(1);
        }
        
        Socket socket = null;
        PrintWriter printWriter = null;
        BufferedReader bufferedReader = null;
        
        try {
            /*
            IP is hard coded, Local Loopback = "127.0.0.1"
            Port is user entry
            */
            socket = new Socket("127.0.0.1", port);
            System.out.println("Conectado...");
            
            OutputStream outputStream = socket.getOutputStream();
            printWriter = new PrintWriter(outputStream, true);
            
            InputStream inputStream = socket.getInputStream();
            InputStreamReader inputStreamReader = 
                    new InputStreamReader(inputStream);
            bufferedReader = new BufferedReader(inputStreamReader);
            
            printWriter.println(args[1]);
            
            String line;
            while((line = bufferedReader.readLine()) != null){
                System.out.println(line);
            };
            
        } catch (IOException ex) {
            System.out.println(ex.toString());
        } finally{
            
            if(bufferedReader != null){
                try {
                    bufferedReader.close();
                    System.out.println("bufferedReader cerrado");
                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
            
            if(printWriter != null){
                printWriter.close();
                System.out.println("printWriter cerrado");
            }
            
            if(socket != null){
                try {
                    socket.close();
                    System.out.println("socket cerrado");
                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
        }
        
    }
    
    private static int isParseInt(String str){
        
        int num = -1;
        try{
             num = Integer.parseInt(str);
        } catch (NumberFormatException e) {
        }
        
        return num;
    }
    
}
