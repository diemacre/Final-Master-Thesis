
/*
 * This file will execute the bluetooth
 * scanner and upload a test case to
 * the database.
 * */

package iitrtclab.snortingblue;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.webkit.WebView;
import android.widget.ProgressBar;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.DataOutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class SecondScreen extends AppCompatActivity {

    /*CONSTANT and VARIABLE DECLARATIONS*/

    private IBeaconScanner testCase;
    public static final String errorDialogKey = "SnortingBlue.errorDialogKey";


    /*METHODS*/

    /*
    * This function will display the information
    * on the previous screen except not allow the
    * user to modify the information. It will
    * also create and upload the test case
    * to the database
    * */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second_screen);

        //Get the test case parameter strings
        try {
            Intent intent = getIntent();
            String X = intent.getStringExtra(FirstScreen.strX);
            String Y = intent.getStringExtra(FirstScreen.strY);
            String Building = intent.getStringExtra(FirstScreen.strBuilding);
            String Floor = intent.getStringExtra(FirstScreen.strFloor);
            String Duration = intent.getStringExtra(FirstScreen.strDur);
            String Minutes  = intent.getStringExtra(FirstScreen.strMin);
            String TestID  = intent.getStringExtra(FirstScreen.strTestID);

            //Get text views
            TextView Xstatic = findViewById(R.id.Xstatic);
            TextView Ystatic = findViewById(R.id.Ystatic);
            TextView BuildingStatic = findViewById(R.id.BuildingStatic);
            TextView DurationStatic = findViewById(R.id.DurationStatic);
            TextView MinutesStatic = findViewById(R.id.MinutesStatic);
            TextView IdStatic = findViewById(R.id.IdStatic);

            //Set the text views to those strings
            Xstatic.setText("X: " + X);
            Ystatic.setText("Y: " + Y);
            BuildingStatic.setText("Building: " + Building + "-" +  Floor);
            DurationStatic.setText("Duration: " + Duration);
            MinutesStatic.setText("Minutes: " + Minutes);
            IdStatic.setText("Id: " + TestID);


            //Recreate the map view
            WebView map = findViewById(R.id.MapStatic);
            MapInterface mapInterface = new MapInterface(this, Xstatic, Ystatic, map);
            map.getSettings().setJavaScriptEnabled(true);
            map.getSettings().setBuiltInZoomControls(true);
            map.setWebViewClient(mapInterface);
            map.addJavascriptInterface(mapInterface, "mapInterface");

            //Set test information
            mapInterface.toggleSettingLocation(false);
            mapInterface.setTestingLocation(Double.parseDouble(X), Double.parseDouble(Y));
            mapInterface.setMap("file:///android_asset/" + Building + "-" + Floor + ".html", Building, Floor);

            //Create bluetooth scanner
            testCase = new IBeaconScanner(this, mapInterface, (ProgressBar)findViewById(R.id.progressBar2), .5);

            //Perform scan
            double x = Double.parseDouble(X);
            double y = Double.parseDouble(Y);
            int floor = Integer.parseInt(Floor);
            int duration = Integer.parseInt(Duration);
            int minutes = Integer.parseInt(Minutes);
            int testID = Integer.parseInt(TestID);
            testCase.start(FirstScreen.BuildingCodes.get(Building), floor, x, y, duration, minutes*60, testID);
        }
        catch(Exception e) {
            finish();
        }
    }


    /*
    * This function will be called when the cancel
    * button is clicked. It will stop the scan and
    * return to the first screen. The results of the
    * scan will not be uploaded to the database.
    * */

    public void Cancel(View view) {
        testCase.stop();
        testCase.finish();
    }



    /*
    * Test Functions
    * */

    /*
    * This will upload a test record to the database.
    * It will log whether or not the upload failed and
    * the reason for the failure.
    * */

    private void UploadRecord() {

        try {
            for(int i = 0; i < 5; i++) {
                URL url = new URL("https://api.iitrtclab.com/test");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                conn.setRequestProperty("Accept", "application/json");
                conn.setDoOutput(true);
                conn.setDoInput(true);

                JSONObject jsonParam = new JSONObject();
                jsonParam.put("major", 1000);
                jsonParam.put("minor", 522);
                jsonParam.put("rssi", -100000);
                jsonParam.put("testID", "FAKE_TEST");
                jsonParam.put("building_id", 5000);
                jsonParam.put("floor", 1);
                jsonParam.put("x", 1234);
                jsonParam.put("y", 1234);
                jsonParam.put("interval", 5);

                Log.i("JSON", jsonParam.toString());
                DataOutputStream os = new DataOutputStream(conn.getOutputStream());

                os.writeBytes(jsonParam.toString());
                os.flush();

                Log.i("STATUS + " + i, String.valueOf(conn.getResponseCode()));
                Log.i("MSG", conn.getResponseMessage());

                os.close();
                conn.disconnect();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    /*
    * This will call UploadRecord on
    * a new thread. UploadRecord
    * has to be called on a thread
    * other than the UI thread.
    * */

    private void UploadRecordTest() {
        new AsyncTask<String, String, String>() {

            @Override
            protected String doInBackground(String... params) {
                try {
                    UploadRecord();
                    return "Success";
                } catch (Exception ex) {
                    ex.printStackTrace();
                    return "";
                }
            }

        }.execute("");
    }
}
