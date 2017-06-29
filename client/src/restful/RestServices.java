package restful;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import org.json.JSONException;
import org.json.JSONObject;


/*Classe que faz conexoes com o servidor restful*/
public class RestServices {
    
    private HttpClient client;//objeto responsavel pela comunicaçao via http  
    private JSONObject services;//objeto json que guarda todos os serviços disponibilizados pelo servidor
    
    /*Construtor da classe.*/
    public RestServices()throws ClientProtocolException, IOException {
        
        client = new DefaultHttpClient();
        services = new JSONObject();
        
        HttpGet request = new HttpGet("http://127.0.0.1:8000/");//vamos acessar a raiz do servidor restful
        HttpResponse response = client.execute(request);//salvamos a resposta
        
        BufferedReader rd = new BufferedReader (new InputStreamReader(response.getEntity().getContent()));
        String line = "";

        while ((line = rd.readLine()) != null) {          
          services = new JSONObject(line);//a resposta do servidor retorna um JSON com cada um dos elementos definindo um serviço no servidor
        }
        
    }
    
    /* Método generico para fazer requisiçoes de GET no servidor restful
       Recebe como parametro a url do serviço desejado. EX: http://127.0.0.1:8000/contas
    */
    public JSONObject getMethod(String url)throws ClientProtocolException, IOException {
        
        JSONObject responseContent = new JSONObject();
        
        HttpGet request = new HttpGet(url);
        HttpResponse response = client.execute(request);
        
        BufferedReader rd = new BufferedReader (new InputStreamReader(response.getEntity().getContent()));
        String line = "";

        while ((line = rd.readLine()) != null) {          
          responseContent = new JSONObject(line);//salvamos cada linha do JSON retornado na resposta do servidor
        }
        
        return responseContent;//retornamos o objeto JSON da resposta  
        
    }
    
    /* Método generico para fazer requisiçoes de POST no servidor restful
       Recebe como parametro a url do serviço desejado e 'data' contendo os dados
       que serao enviados ao servidor. EX: http://127.0.0.1:8000/contas/1/
    */
    public JSONObject postMethod(String url, JSONObject data)throws ClientProtocolException, IOException{
        
        JSONObject responseContent = new JSONObject();
        
        HttpPost post = new HttpPost(url);
        StringEntity input = new StringEntity(data.toString());//colocamos os dados json na request que sera enviada pelo POST
        input.setContentType("application/json");//definimos o mime type
        post.setEntity(input);
        
        HttpResponse response = client.execute(post);//envia o POST e ja salva a resposta do servidor
        
        BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line = "";
        
        while ((line = rd.readLine()) != null) {
         responseContent = new JSONObject(line);//a resposta retorna o novo objeto json criado no servidor.
        }
        return responseContent;
    }
    
    /* Método generico para fazer requisiçoes de PUT no servidor restful
       Recebe como parametro a url do serviço desejado e 'data' contendo os dados
       que serao enviados ao servidor. EX: http://127.0.0.1:8000/contas/1/
    */
    public JSONObject putMethod(String url, JSONObject data)throws ClientProtocolException, IOException{
        JSONObject responseContent = new JSONObject();
        
        HttpPut put = new HttpPut(url);
        StringEntity input = new StringEntity(data.toString());//colocamos os dados json na request que sera enviada pelo PUT
        input.setContentType("application/json");//definimos o mime type
        put.setEntity(input);
        
        HttpResponse response = client.execute(put);//envia o PUT e ja salva a resposta do servidor
        
        BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line = "";
        
        while ((line = rd.readLine()) != null) {
            responseContent = new JSONObject(line);//a resposta retorna o objeto json modificado no servidor.
        }
        return responseContent;//retornamos o objeto json modificado
        
    }

//serviços disponiveis no servidor
    public JSONObject getServices() {
        return services;
    }    
}
