package iitrtclab.snortingblue;

import java.util.LinkedList;

/**
 * Created by enzop on 25/05/2017.
 * Edited by Yuyang on 26/02/2018
 */

public class IBeacon {
    private int major, minor;
    private String uuid;
    private LinkedList<Integer> rssiSet;
    private double x, y;

    /* CONSTRUCTORS */

    public IBeacon(int rssi, int major, int minor, String uuid) {
        rssiSet = new LinkedList<>();
        rssiSet.add(rssi);
        this.major = major;
        this.minor = minor;
        this.uuid = uuid;
    }

    /* GETTERS AND SETTERS */

    public int getRssi() {
        int sum = 0;
        for (int x:rssiSet)
            sum+=x;
        return sum/rssiSet.size();
    }

    public void add(int rssi) {
        rssiSet.add(rssi);
    }

    public int getMajor() {
        return major;
    }

    public void setMajor(int major) {
        this.major = major;
    }

    public int getMinor() {
        return minor;
    }

    public void setMinor(int minor) {
        this.minor = minor;
    }

    public void setPosition(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public String getUuid() {
        return uuid;
    }

    public void setUuid(String uuid) {
        this.uuid = uuid;
    }
    public long getKey(){
        return getKey(major,minor);
    }
    public static long getKey(int major,int minor){
        return Long.parseLong(""+major+minor);
    }

    @Override
    public String toString() {
        return "IBeacon{" +
                "rssi=" + getRssi() +
                ", major=" + major +
                ", minor=" + minor +
                ", uuid='" + uuid + '\'' +
                '}';
    }
}
