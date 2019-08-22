
/*
* This file is used for safely running
* the MapInterface functions. MapInterface
* functions will not run properly until the
 * map has finished loading.
* */

package iitrtclab.snortingblue;

import android.widget.TextView;

import java.lang.Runnable;

public abstract class MapRunnable implements Runnable {

    MapInterface master;
    boolean enableLocSetting = false;
    int major, minor, rssi;
    double x, y;
    TextView xView, yView;
    String path;

    public MapRunnable(MapInterface master) {
        this.master = master;
    }

    public MapRunnable(boolean enableLocSetting, MapInterface master) {
        this.master = master;
        this.enableLocSetting = enableLocSetting;
    }

    public MapRunnable(int major, int minor, int rssi, MapInterface master) {
        this.major = major;
        this.minor = minor;
        this.master = master;
    }

    public MapRunnable(double x, double y, MapInterface master) {
        this.x = x;
        this.y = y;
        this.master = master;
    }

    public MapRunnable(double x, double y, TextView xView, TextView yView, MapInterface master) {
        this.x = x;
        this.y = y;
        this.xView = xView;
        this.yView = yView;
        this.master = master;
    }

    public MapRunnable(String path, MapInterface master) {
        this.path = path;
        this.master = master;
    }

    public abstract void run();
}
