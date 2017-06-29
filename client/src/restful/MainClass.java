package restful;
import gui.TelaLogin;
import java.io.IOException;
import org.apache.http.client.ClientProtocolException;


public class MainClass {
    
    public static void main(String[] args) throws ClientProtocolException, IOException{
        
        RestServices rest = new RestServices();//instanciamos o objeto restful
                
        new TelaLogin(rest); //tela login para indicar conta e agencia que sera acessada
    }
}
