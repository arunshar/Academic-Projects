package edu.buffalo.cse.cse486586.groupmessenger2;

import java.io.Serializable;
import java.util.Comparator;

/**
 * Created by Arun on 3/16/2017.
 */

public class Message_info {
    Integer msgid;
    String msgtext;
    Integer clientport;
    Integer serverport;
    Boolean deliverable;
    Integer locseq;

    public Message_info(Integer msgid, String msgtext, int clientport, int serverport, Boolean deliverable, Integer locseq){
        this.msgid = msgid;
        this.msgtext = msgtext;
        this.clientport = clientport;
        this.serverport = serverport;
        this.deliverable = deliverable;
        this.locseq = locseq;
    }

    @Override
    public boolean equals(Object o){
        if(this.msgid==((Message_info) o).msgid){
            return true;
        }
        return false;
    }
}

