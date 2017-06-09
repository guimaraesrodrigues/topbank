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

public class RestServices {
    
    private HttpClient client;  
    private JSONObject services;
    
    public RestServices()throws ClientProtocolException, IOException {
        
        client = new DefaultHttpClient();
        services = new JSONObject();
        
        HttpGet request = new HttpGet("http://127.0.0.1:8000/");
        HttpResponse response = client.execute(request);
        
        BufferedReader rd = new BufferedReader (new InputStreamReader(response.getEntity().getContent()));
        String line = "";

        while ((line = rd.readLine()) != null) {          
          services = new JSONObject(line);
        }
        
    }
    
    public JSONObject getMethod(String url)throws ClientProtocolException, IOException {
        
        JSONObject responseContent = new JSONObject();
        
        HttpGet request = new HttpGet(url);
        HttpResponse response = client.execute(request);
        
        BufferedReader rd = new BufferedReader (new InputStreamReader(response.getEntity().getContent()));
        String line = "";

        while ((line = rd.readLine()) != null) {          
          responseContent = new JSONObject(line);
        }
        
        return responseContent;        
        
    }
    
    
    public JSONObject postMethod(String url, JSONObject data)throws ClientProtocolException, IOException{
        
        JSONObject responseContent = new JSONObject();
        
        HttpPost post = new HttpPost(url);
        StringEntity input = new StringEntity(data.toString());
        input.setContentType("application/json");
        post.setEntity(input);
        
        HttpResponse response = client.execute(post);
        
        BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line = "";
        
        while ((line = rd.readLine()) != null) {
         responseContent = new JSONObject(line);
        }
        return responseContent;
    }
    
    
    public JSONObject putMethod(String url, JSONObject data)throws ClientProtocolException, IOException{
        JSONObject responseContent = new JSONObject();
        
        HttpPut put = new HttpPut(url);
        StringEntity input = new StringEntity(data.toString());
        input.setContentType("application/json");
        put.setEntity(input);
        
        HttpResponse response = client.execute(put);
        
        BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line = "";
        
        while ((line = rd.readLine()) != null) {
            responseContent = new JSONObject(line);
        }
        return responseContent;
        
    }


    public JSONObject getServices() {
        return services;
    }    
}
