import java.net.Socket;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.io.InputStreamReader;
import java.io.IOException;
import org.json.JSONObject;
import org.json.JSONException;

class TestCommandServer{
    
    public static void main(String[] args) throws IOException{
        try(
            Socket socket = new Socket("127.0.0.1", 4444);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        ){
            //in order to test on your machine this path must be changed because duh
            // String filePath = "/home/greg/code/Server/tests/output/";
            String filePath = "/home/ericj1s/Capstone/Server/output";
            //test Go command
            JSONObject obj = new JSONObject();
            // obj.put("command", "go");
            // out.println(obj.toString());
            // System.out.println(in.readLine());
            
            obj = new JSONObject();
            obj.put("command", "go");
            obj.put("filePath", filePath);
            out.println(obj.toString());
            System.out.println(in.readLine());
            
            boolean done = false;
            do{
                try{
                    Thread.sleep(30000);
                } catch (InterruptedException e) {
                    System.out.println("sleep interrupted");
                }
                //test ProgressReport command
                obj = new JSONObject();
                obj.put("command", "progressReport");
                out.println(obj.toString());
                JSONObject response = new JSONObject(in.readLine());
                System.out.println(response.toString());
                System.out.println("Status: " + response.getString("status") + "\nProgress: " + response.getDouble("progress"));
                
                done = response.getDouble("progress") == 1.0;
            }while(!done);
            
            //test End command
            obj = new JSONObject();
            obj.put("command","end");
            out.println(obj.toString());
            System.out.println(in.readLine());
        }
        catch(IOException e){
            System.out.println("Exception caught when trying to write to port 4444");
            System.err.println(e.getMessage());
        }
        catch(JSONException e){
            System.out.println("Exception caught when trying to create JSONObject");
            System.err.println(e.getMessage());
        }
    }
}
