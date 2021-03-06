import java.net.ServerSocket;
import java.net.Socket;
import java.io.DataOutputStream;
import java.io.DataInputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.lang.AutoCloseable;
import org.json.JSONObject;
import org.json.JSONException;

class CommandServer implements AutoCloseable{
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private DataOutputStream out;
    private DataInputStream in;
    
    public CommandServer(int portNum) throws IOException{
        this.serverSocket = new ServerSocket(portNum);
        this.clientSocket = serverSocket.accept();
        this.out = new DataOutputStream(clientSocket.getOutputStream());
        this.in = new DataInputStream(clientSocket.getInputStream()); 
    }
    
    public void close() throws IOException{
        serverSocket.close();
        clientSocket.close();
        out.close();
        in.close();
	
    }
 
    public void run(){
       try{  
            boolean run = true;
            ImageProcessor processor;
            ProgressWrapper progress = null;
            while(run){
			    byte[] message = new byte[1024];
			    in.read(message);
			    String input = new String(message);
                if(input != null){
                    JSONObject obj = new JSONObject(input);
                    if(obj.has("command")){
                        JSONObject response = new JSONObject();
                        switch(obj.getString("command")){
                            case "go":
                                if(obj.has("filePath")){
                                    String filePath = obj.getString("filePath");
                                    //Do stuff
                                    progress = new ProgressWrapper();
                                    processor = new ImageProcessor(filePath, progress);
                                    processor.start();
                                    System.out.println("Process Images");
                                    System.out.println("Create CSVs at " + filePath);
                                
                                    response.put("response","commandExecuted");
                                }
                                else{
                                    response.put("response", "error");
                                    response.put("message", "No file path provided with go command. See API.");
                                }
                                break;
                                
                            case "progressReport":
                                //get progress from ImageProcessor and create response
                                float completed = 0;
                                if (progress != null) {
                                    completed = progress.getProgress();
                                    //System.out.println("checked progress");
                                }
                                
                                response.put("response", "progressReport");                            
                                response.put("status", "running");
                                response.put("progress", completed);
                                break;

                            case "stopProcess":
                                //stop
                                response.put("response", "commandExecuted");                            
                                break;
                                
                            case "end":
                                run = false;
                                response.put("response", "commandExecuted");
                                break;
                        }
                        out.write(response.toString().getBytes());
                    }
                }
            }
        }
        catch(IOException e){
            System.err.println("ERROR READING COMMAND FROM PORT");
            System.err.println(e.getMessage());
        }
        catch(JSONException e){
            System.err.println("ERROR WHEN CREATING JSONOBJECT");
            System.err.println(e.getMessage());
        }
    }
    
     public static void main(String[] args){
        try(CommandServer cmdServer = new CommandServer(4444))
        {
            cmdServer.run();
            cmdServer.close();
        }
        catch(IOException e){
            System.err.println("ERROR CREATING COMMAND SERVER");
            System.err.println(e.getMessage());
        }
    }
}
