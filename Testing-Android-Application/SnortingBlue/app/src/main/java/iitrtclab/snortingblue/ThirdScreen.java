

/*
* This screen will be called if an error occurred
* during bluetooth uploading. This screen will display
* a TextView with an error log of what happened.
* */


package iitrtclab.snortingblue;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.TextView;

public class ThirdScreen extends AppCompatActivity {

    /*
    * This function will create the third screen
    * and load the TextView object with the
    * error dialog.
    * */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_third_screen);

        Intent intent = getIntent();
        TextView ErrorDialog = findViewById(R.id.ErrorDialog);
        ErrorDialog.setMovementMethod(new ScrollingMovementMethod());

        String errorDialog = intent.getStringExtra(SecondScreen.errorDialogKey);
        ErrorDialog.setText(errorDialog);
    }

    /*
     * This function will be called when the
     * Done button is clicked. It will return
     * the user back to the first screen.
     * */

    public void Done(View view) {
        finish();
    }
}
