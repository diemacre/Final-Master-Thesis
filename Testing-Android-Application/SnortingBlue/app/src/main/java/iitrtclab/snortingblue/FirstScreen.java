
/*
* The way this program works is as follows:
*   1. The user will input their test information into the first screen
*       - Position of the tester: (Building, Floor, x, y)
*       - Duration: the number of seconds to scan for
*   2. They will click the "start" button, get them to the second
*      screen and start a bluetooth scan
*       - The second screen will replace the start button with a progress bar.
*       - If the user presses the cancel button, the test case will end and the
*         user will be taken back to the first screen
*       - If the scan completes, the test case will end and the user
*         will be taken back to the first screen
*   3. During the bluetooth scan, we will compile a list of all nearby bluetooth
*      devices and their signal strengths. This list will be updated every 500ms
*      over a user-defined period of time.
*   4. After the scan finishes, we will upload the following records to the database:
*       [Test Case ID][Building][floor_true][x_true][y_true][Scan Period][Major][Minor][RSSI]
*       - NOTE: test case IDs will be randomly generated. This **may** produce conflicts
*         in the test cases.
* */

/*
* This file will allow users to define the parameters of a test case:
*   - Position of the tester: (Building, floor_true, x_true, y_true)
*   - Duration: the number of seconds to scan for
*
*   NOTE: I'm trying to make it so that the test app can send the position of the beacons to the
*   database as well. This will require renderBeaconByMajorMinor to do a little more work. I modified
*   the "run" function in IBeaconScanner to do this.
* */

package iitrtclab.snortingblue;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import java.util.HashMap;
import java.util.Hashtable;

public class FirstScreen extends AppCompatActivity  {

    /*CONSTANTS and VARIABLE DECLARATIONS*/


    //Context management
    Context context;

    //Keys for the inputs
    public static final String strX = "SnortingBlue.X";
    public static final String strY = "SnortingBlue.Y";
    public static final String strBuilding = "SnortingBlue.Building";
    public static final String strFloor = "SnortingBlue.Floor";
    public static final String strDur = "SnortingBlue.Duration";
    public static final String strMin = "SnortingBlue.Minutes";
    public static final String strTestID = "SnortingBlue.TestID";

    //The list of buildings
    public static final String[] Buildings = {"Building", "AM", "IS", "KI", "SB"};

    //The lists of possible floors
    public static final String[] floors0 = {"Floor"};
    public static final String[] floors1 = {"Floor", "00"};
    public static final String[] floors2 = {"Floor", "00", "01"};
    public static final String[] floors3 = {"Floor", "00", "01", "02"};

    //Building HashMaps
    public static final Hashtable<String, String[]> BuildingToFloors = new Hashtable<String, String[]>();
    public static final Hashtable<String, Integer> BuildingCodes = new Hashtable<String, Integer>();

    //The javascript interface to manipulating the map
    MapInterface mapInterface;

    //The default map
    public static final String default_map = "file:///android_asset/default.html";


    /*METHODS*/

    /*
    * This function will check the permissions
    * at the inception of the application. It
    * will make sure that your bluetooth and
    * location services are enabled.
    * */

    private void PermissionsCheck() {
        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
            finish();
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.BLUETOOTH},
                    1);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_ADMIN) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.BLUETOOTH_ADMIN},
                    2);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                    3);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    4);
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.INTERNET},
                    5);
        }
    }


    /*
    * This function will create the fields for creating
    * a test case.
    * */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first_screen);

        //Permissions check
        PermissionsCheck();

        //Save context
        context = this;

        //Define how many floors each building has
        BuildingToFloors.put(Buildings[0], floors0);
        BuildingToFloors.put(Buildings[1], floors3);
        BuildingToFloors.put(Buildings[2], floors3);
        BuildingToFloors.put(Buildings[3], floors3);
        BuildingToFloors.put(Buildings[4], floors3);

        //Define the building codes
        BuildingCodes.put("Building", -1);
        BuildingCodes.put("SB", 31);
        BuildingCodes.put("AM", 4);
        BuildingCodes.put("IS", 64);
        BuildingCodes.put("KI", 65);

        //Set building spinner callback
        Spinner BuildingList = findViewById(R.id.Building);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(context, android.R.layout.simple_spinner_dropdown_item, Buildings);
        BuildingList.setAdapter(adapter);
        BuildingList.setOnItemSelectedListener(BuildingSpinnerCB);

        //Set floor spinner callback
        Spinner FloorList = findViewById(R.id.Floor);
        adapter = new ArrayAdapter<>(context, android.R.layout.simple_spinner_dropdown_item, BuildingToFloors.get("Building"));
        FloorList.setAdapter(adapter);
        FloorList.setOnItemSelectedListener(FloorSpinnerCB);

        //Create the map
        WebView map = findViewById(R.id.Map);
        mapInterface = new MapInterface(this, (TextView)findViewById(R.id.X), (TextView)findViewById(R.id.Y), map);
        map.getSettings().setJavaScriptEnabled(true);
        map.getSettings().setBuiltInZoomControls(true);
        map.setWebViewClient(mapInterface);
        map.addJavascriptInterface(mapInterface, "mapInterface");
    }


    /*
    * This function will update the map to the new bulding/floor
    * combination. This will be called whenever the building or floor
    * is changed.
    * */

    public void UpdateMap(String building, String floor) {
        WebView map = findViewById(R.id.Map);
        String path = "file:///android_asset/" + building + "-" + floor + ".html";

        if(map.getUrl() != null)
            if(map.getUrl().equals(path))
                return;

        try {
            System.out.println("SETTING MAP???");
            getResources().getAssets().open(building + "-" + floor + ".html");
            mapInterface.toggleSettingLocation(true);
            mapInterface.setTestingLocation(0,0);
            mapInterface.setMap(path, building, floor);
        }
        catch(Exception e) {
            if(map.getUrl() != null)
                if(!map.getUrl().equals(default_map))
                    mapInterface.setMap(default_map, "Building", "Floor");
        }
    }



    /*
    * This function will be called when the
    * start button is pressed.
    * */

    public void Start(View view) {
        try {
            Intent intent = new Intent(this, SecondScreen.class);

            //Retrieve the inputs to the test case
            TextView X = findViewById(R.id.X);
            TextView Y = findViewById(R.id.Y);
            Spinner Building = findViewById(R.id.Building);
            Spinner Floor = findViewById(R.id.Floor);
            EditText Duration = findViewById(R.id.Duration);
            EditText Minutes = findViewById(R.id.Minutes);
            EditText TestID = findViewById(R.id.TestID);

            //Give the inputs to the second screen
            intent.putExtra(strX, X.getText().toString());
            intent.putExtra(strY, Y.getText().toString());
            intent.putExtra(strBuilding, Building.getSelectedItem().toString());
            intent.putExtra(strFloor, Floor.getSelectedItem().toString());
            intent.putExtra(strDur, Duration.getText().toString());
            intent.putExtra(strMin, Minutes.getText().toString());
            intent.putExtra(strTestID, TestID.getText().toString());

            //Make sure that the map is valid
            WebView map = findViewById(R.id.Map);
            if (map.getUrl().equals(default_map))
                return;

            //Launch second screen
            startActivity(intent);
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    }








    /*CALLBACK FUNCTIONS*/

    /*
     * This function represents the action that occurs when the dropdown menu
     * for buildings is used. It will update the map to the new building/floor
     * combo. It will also update the list of floors that appear in the
     * floor dropdown menu.
     */
    private final AdapterView.OnItemSelectedListener BuildingSpinnerCB = new AdapterView.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int pos,
                                   long id) {
            try {
                String building = parent.getItemAtPosition(pos).toString();

                Spinner BuildingFloors = findViewById(R.id.Floor);
                ArrayAdapter<String> adapter = new ArrayAdapter<String>(context, android.R.layout.simple_spinner_dropdown_item, BuildingToFloors.get(building));
                BuildingFloors.setAdapter(adapter);
                UpdateMap(building, "0");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onNothingSelected(AdapterView<?> arg0) {
        }
    };



    /*
     * This function represents the action that occurs when the
     * floor is changed. It will update the map to be the new
     * floor.
     * */
    private final AdapterView.OnItemSelectedListener FloorSpinnerCB = new AdapterView.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
            try {
                Spinner Building = findViewById(R.id.Building);
                String building = Building.getSelectedItem().toString();
                UpdateMap(building, parent.getItemAtPosition(pos).toString());
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onNothingSelected(AdapterView<?> arg0) {
        }
    };


}
