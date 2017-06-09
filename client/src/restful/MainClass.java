package restful;
import gui.TelaLogin;
import java.io.IOException;
import org.apache.http.client.ClientProtocolException;


public class MainClass {
    
    public static void main(String[] args) throws ClientProtocolException, IOException{
        
        RestServices rest = new RestServices();
                
        new TelaLogin(rest); 
    }
}
