import java.lang.Thread;
   
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

//--------- GPIO ------------------
import com.pi4j.io.gpio.*;
import com.pi4j.io.gpio.event.GpioPinDigitalStateChangeEvent;
import com.pi4j.io.gpio.event.GpioPinListenerDigital;
import com.pi4j.platform.PlatformAlreadyAssignedException;
import com.pi4j.util.CommandArgumentParser;
import com.pi4j.util.Console;
import com.pi4j.util.ConsoleColor;

import java.util.concurrent.Future;


public class RaspberryJavaServer {

    //boolean static start = false;

    public static void main(String[] args) throws InterruptedException, PlatformAlreadyAssignedException {
        System.out.println("Server start");
        System.out.println("Runtime Java: " 
                + System.getProperty("java.runtime.version"));
        
        ServerSocket serverSocket = null;
        Socket clientSocket = null;
        BufferedReader bufferedReader = null;
        PrintWriter printWriter = null;


        // crear wrapper/helper de consola Pi4J
        final Console console = new Console(); // (This is a utility class to abstract some of the boilerplate code)
        console.promptForExit(); // allow for user to exit program using CTRL-C

     //-------------------- INPUT --------------------------------------------------------------------
        final GpioController gpioIn = GpioFactory.getInstance(); // crear controlador de GPIO
        //Predeterminadamente usaremos el pin #29
        //pero si argumento ha sido introducido, entonces se usara ese pin 
        Pin pin29 = CommandArgumentParser.getPin(
                RaspiPin.class,    // clase de proveedor para obtener instancia de pin
                RaspiPin.GPIO_21,  // pin predeterminado si no es introducido algun argumento
                args);             // arreglo de argumentos para revisar

        // Predeterminadamente usaremos PULL-UP en el pin GPIO 
        // pero si argumento ha sido introducido, entonces se usara la resistencia pull especificada
        PinPullResistance pull29 = CommandArgumentParser.getPinPullResistance(
                PinPullResistance.PULL_UP,  // resistencia pull predeterminado si no es introducido algun argumento
                args);                      // arreglo de argumentos para revisar

        // GPIO pin como input pin
        final GpioPinDigitalInput input = gpioIn.provisionDigitalInputPin(pin29, "MyInput", pull29);

        // establecer estado shutdown para este pin: unexport el pin
        input.setShutdownOptions(true);

        // crear y registrar GPIO pin listener
        input.addListener(new GpioPinListenerDigital() {
            @Override
            public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
                // enseñar estado de pin en la consola
                System.out.println(" --> GPIO PIN STATE CHANGE: " + event.getPin() + " = " + event.getState());

                
                
            }

        });


     //------------- OUPUT --------------------------------
        // crear controlador de GPIO
        final GpioController gpioOut = GpioFactory.getInstance();

        //Predeterminadamente usaremos el pin #31
        //pero si argumento ha sido introducido, entonces se usara ese pin 
        Pin pin31 = CommandArgumentParser.getPin(
                RaspiPin.class,    // clase de proveedor para obtener instancia de pin
                RaspiPin.GPIO_22,  // pin predeterminado si no es introducido algun argumento
                args);             // arreglo de argumentos para revisar

        // gpio pin como output pin y prenderlo
        final GpioPinDigitalOutput output31 = gpioOut.provisionDigitalOutputPin(pin31, "My Output", PinState.HIGH);

        // establecer estado de shutdown para este pin: deja como output pin, pon en estado low
        output31.setShutdownOptions(false,PinState.LOW,PinPullResistance.OFF);

        // crear pin listener para imprimir los cambios al estado output del GPIO pin 
        output31.addListener(new GpioPinListenerDigital() {
            @Override
            public void handleGpioPinDigitalStateChangeEvent(GpioPinDigitalStateChangeEvent event) {
                // enseñar estado de pin en consola
                console.println(" --> GPIO PIN STATE CHANGE: " + event.getPin() + " = " +
                        ConsoleColor.conditional(
                                event.getState().isHigh(), // expresion condicional
                                ConsoleColor.GREEN,        // color de condicion positiva
                                ConsoleColor.RED,          // color de condicion negativa
                                event.getState()));        // text to display

                if(event.getState().isHigh()){

                }
                else{

                }
            }
        });

        try {

	    /*while(!start){
                 Thread.sleep(2000);
	    }	*/	

            serverSocket = new ServerSocket(8000);  //Puerto del servidor
            System.out.println("Server port: " 
                    + serverSocket.getLocalPort());

            clientSocket = serverSocket.accept();
            
            //Cliente conectado
            output31.toggle();
            InputStream inputStream = clientSocket.getInputStream();    //Entrada
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            bufferedReader = new BufferedReader(inputStreamReader);
            
            OutputStream outputStream = clientSocket.getOutputStream(); //Salida
            printWriter = new PrintWriter(outputStream, true);

            String line;
            while((line = bufferedReader.readLine()) != null){  //Leer lo que fue escrito
                System.out.println(line);   //Imprimir mensaje en pantalla
                printWriter.println(line);  //echo de regreso al que mando mensaje
            }
        } 
	catch (IOException ex) {
            System.err.println(ex.toString());
	}
	finally{
            
            if(printWriter != null){
                printWriter.close();
                System.out.println("printWriter closed");
            }
            
            if(bufferedReader != null){
                try {
                    bufferedReader.close();
                    System.out.println("bufferedReader closed");
                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
            
            if(clientSocket != null){
                try {
                    clientSocket.close();
                    System.out.println("clientSocket closed");
                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
            
            if(serverSocket != null){
                try {
                    serverSocket.close();
                    System.out.println("serverSocket closed");
                    output31.toggle();
                    // para toda actividad/threads GPIO apagando el controlador de GPIO
                    // (este metodo forza un shutdown a todos los GPIO monitoriando los threads y scheduled tasks)
                    gpioIn.shutdown();
		    gpioOut.shutdown();

                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
            
        }
        
    }
    
}
     
