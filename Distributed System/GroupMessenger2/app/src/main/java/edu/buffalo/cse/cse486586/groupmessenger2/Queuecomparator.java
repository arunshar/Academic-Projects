package edu.buffalo.cse.cse486586.groupmessenger2;

import android.nfc.Tag;
import android.util.Log;

import java.util.Comparator;

import static edu.buffalo.cse.cse486586.groupmessenger2.GroupMessengerActivity.TAG;

/**
 * Created by jarvis on 3/24/17.
 */

public class Queuecomparator implements Comparator<Message_info> {
    @Override
    public int compare(Message_info lhs, Message_info rhs) {

        if (lhs.locseq == rhs.locseq) {

            if (lhs.clientport <= rhs.clientport) { return -1;}
            else {return 1;}

        } else if (lhs.locseq <= rhs.locseq) {
            return -1;
        } else {return 1;}
    }
}

