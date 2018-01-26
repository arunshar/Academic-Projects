package edu.buffalo.cse.cse486586.groupmessenger2;

import android.app.Activity;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.InterfaceAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Comparator;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.io.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.PriorityBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;

import static android.util.Log.d;
import static android.util.Log.println;
import static edu.buffalo.cse.cse486586.groupmessenger2.R.id.remote_text_display;

/**
 * GroupMessengerActivity is the main Activity for the assignment.
 *
 * @author stevko
 */
public class GroupMessengerActivity extends Activity {

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    static int msgidNo = 0;
    static int propsec = 0;

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.activity_group_messenger, menu);
        return true;
    }

    static final String TAG = GroupMessengerActivity.class.getSimpleName();
    static final int SERVER_PORT = 10000;
    static final String ports[] = {"11108", "11112", "11116", "11120", "11124"};
    CopyOnWriteArrayList<String> ACTIVE_PORTS = new CopyOnWriteArrayList<String>();
    CopyOnWriteArrayList<String> DEAD_PORTS = new CopyOnWriteArrayList<String>();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_group_messenger);
        for(String port : ports){
            ACTIVE_PORTS.add(port);
        }
        TelephonyManager tel = (TelephonyManager) this.getSystemService(Context.TELEPHONY_SERVICE);
        String portStr = tel.getLine1Number().substring(tel.getLine1Number().length() - 4);
        final String myPort = String.valueOf((Integer.parseInt(portStr) * 2));

        try {

            ServerSocket serverSocket = new ServerSocket(SERVER_PORT);
            new ServerTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, serverSocket);
        } catch (IOException e) {

            Log.e(TAG, "Can't create a ServerSocket");
            return;
        }

        final EditText editText = (EditText) findViewById(R.id.editText1);

        Button sendtext = (Button) findViewById(R.id.button4);
        String msg = editText.getText().toString();


        /*
         * TODO: Use the TextView to display your messages. Though there is no grading component
         * on how you display the messages, if you implement it, it'll make your debugging easier.
         */
        TextView tv = (TextView) findViewById(R.id.textView1);
        tv.setMovementMethod(new ScrollingMovementMethod());

        /*
         * Registers OnPTestClickListener for "button1" in the layout, which is the "PTest" button.
         * OnPTestClickListener demonstrates how to access a ContentProvider.
         */
        findViewById(R.id.button1).setOnClickListener(
                new OnPTestClickListener(tv, getContentResolver()));


        /*
         * TODO: You need to register and implement an OnClickListener for the "Send" button.
         * In your implementation you need to get the message from the input box (EditText)
         * and send it to other AVDs.
         */
        sendtext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String msg = editText.getText().toString() + "\n";
                editText.setText("");
                new ClientTask().executeOnExecutor(AsyncTask.SERIAL_EXECUTOR, msg, myPort);
            }
        });
    }

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */

    String sendersport;
    String recieversport;
    int msgid;
    String msgtext;
    Boolean deliverable;
    int counter = 0;
    int locseq = 0;

    Comparator<Message_info> obj1 = new Queuecomparator();
    PriorityBlockingQueue<Message_info> deliveryqueue = new PriorityBlockingQueue<Message_info>(50, obj1);
    AtomicInteger count = new AtomicInteger(0);
    private class ServerTask extends AsyncTask<ServerSocket, String, String> {

        @Override
        protected String doInBackground(ServerSocket... sockets) {

            ServerSocket serverSocket = sockets[0];
            d(TAG, "Server");
            try {
                while (true) {
                    counter = counter + 1;
                    Socket clientsocket = serverSocket.accept();
                    try {
                        BufferedReader inserver = new BufferedReader(new InputStreamReader(clientsocket.getInputStream()));
                        BufferedWriter outserver = new BufferedWriter(new OutputStreamWriter(clientsocket.getOutputStream()));


                        Log.d(TAG, "message recieved from client");
                        String message = inserver.readLine();
                        outserver.write("OK1");
                        outserver.write("OK");
                        outserver.flush();
                        //d(TAG, "final msg recieved after multicast : " + message);

                        // saari string ko float mein convert karna
                        String[] inputs = message.split(",");
                        int msgid = Integer.parseInt(inputs[0]);
                        locseq = Integer.parseInt(inputs[1]);
                        int sendersport = Integer.parseInt(inputs[2]);
                        int recieversport = Integer.parseInt(inputs[3]);
                        deliverable = Boolean.parseBoolean(inputs[4]);
                        String z = inputs[5];
                        msgtext = inputs[6];


                        if(z.equals("a")) {
                            Message_info agreedobj = new Message_info(msgid, msgtext, sendersport, recieversport, deliverable, locseq);
                            Iterator<Message_info> iter = deliveryqueue.iterator();
                            Log.d(TAG, "hobackqueue size : " + deliveryqueue.size());


                            Log.d(TAG, "Hola");
                            propsec = Math.max(propsec, agreedobj.locseq);
                            while (iter.hasNext()) {
                                Message_info j = iter.next();
                                if (j.msgid.equals(agreedobj.msgid)) {
                                    iter.remove();
                                }
                                else if(DEAD_PORTS.contains(String.valueOf(j.clientport))){
                                    iter.remove();
                                }
                            }

                            agreedobj.deliverable=true;
                            deliveryqueue.add(agreedobj);
                            Log.e(TAG,"Size of the queue : "+deliveryqueue.size());

                            //Log.d(TAG, "j sequence : " + j.locseq);
                            Log.d(TAG,DEAD_PORTS.toString());
                            Iterator<Message_info> iter1 = deliveryqueue.iterator();


                        }
                        else if(z.contains("b")) {
                            propsec = propsec + 1;
                            Message_info unicastobj = new Message_info(msgid, msgtext , sendersport, recieversport, deliverable, locseq);
                            if(unicastobj.locseq<propsec)
                                unicastobj.locseq = propsec;
                            deliveryqueue.add(unicastobj);


                            String stringpropmax = Integer.toString(propsec);
                            String stringdeliverable = String.valueOf(deliverable);

                            String clientsport = Integer.toString(sendersport);
                            String serversport = Integer.toString(recieversport);

                            String messageDataUnicast = unicastobj.msgid + "," + stringpropmax + "," +sendersport+ "," + recieversport + "," + stringdeliverable + "," + msgtext;

                            outserver.write(messageDataUnicast);

                        }
                        Log.e(TAG, "This is it !!! ");
                        while (deliveryqueue.size() > 0 && deliveryqueue.peek() != null) {
                            if(DEAD_PORTS.contains(String.valueOf(deliveryqueue.peek().clientport)))
                                deliveryqueue.poll();
                            else if (deliveryqueue.peek().deliverable) {
                                Message_info finalreadyobject = deliveryqueue.poll();
                                String readyId = Integer.toString(finalreadyobject.msgid);
                                if(deliveryqueue.size() > 0){
                                    Log.e(TAG, "New queue size : " + deliveryqueue.size());
                                }
                                String maxsequence = Integer.toString(finalreadyobject.locseq);
                                String finalmessage = finalreadyobject.msgtext;
                                publishProgress(finalmessage);
                                if (deliveryqueue.size() > 0 ){
                                    while (deliveryqueue.size() > 0 && deliveryqueue.peek() != null){
                                        if(DEAD_PORTS.contains(String.valueOf(deliveryqueue.peek().clientport))){
                                            deliveryqueue.poll();
                                        }
                                        else if(deliveryqueue.peek().deliverable){
                                            publishProgress(deliveryqueue.poll().msgtext);
                                        } else {
                                            break;
                                        }
                                    }

                                }
                            } else {
                                break;
                            }
                        }


                        outserver.flush();
                        outserver.close();
                        inserver.close();
                        clientsocket.close();


                    } catch (IOException e){
                        e.printStackTrace();
                    }catch (NullPointerException e){
                        e.printStackTrace();
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            /*
             * TODO: Fill in your server code that receives messages and passes them
             * to onProgressUpdate().
             */

            return null;

        }

        private Uri buildUri(String scheme, String authority) {
            Uri.Builder uriBuilder = new Uri.Builder();
            uriBuilder.authority(authority);
            uriBuilder.scheme(scheme);
            return uriBuilder.build();
        }


        protected void onProgressUpdate(String... strings) {
            /*
             * The following code displays what is received in doInBackground().
             */

            String strReceived = strings[0].trim();
            TextView remoteTextView = (TextView) findViewById(remote_text_display);
            remoteTextView.append(strReceived + "\t\n");
            TextView localTextView = (TextView) findViewById(R.id.textView1);
            localTextView.append("\n");


            Uri mUri = buildUri("content", "edu.buffalo.cse.cse486586.groupmessenger2.provider");
            ContentValues cv = new ContentValues();
            ContentResolver cr = getContentResolver();
            cv.put("key", count.getAndIncrement());
            cv.put("value", strReceived);
            cr.insert(mUri, cv);

            String filename = "SimpleMessengerOutput";
            String string = strReceived + "\n";
            FileOutputStream outputStream;

            try {
                outputStream = openFileOutput(filename, Context.MODE_PRIVATE);
                outputStream.write(string.getBytes());
                outputStream.close();
            } catch (Exception e) {
                Log.e(TAG, "File write failed");
            }

            return;
        }
    }


    private class ClientTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... msgs) {
            int propmax = 0;
            String msgready = msgs[0];
            int msgno = msgidNo;
            String senderport = msgs[1];
            String msgid = senderport + String.valueOf(msgno);
            msgidNo = msgidNo + 1;
            int count = 0;
            String locseq1 = Integer.toString(locseq);
            int maxagreed = 0;
            deliverable = false;
            String status = String.valueOf(deliverable);
            Boolean status1 = false;
            Log.d("Client:", "RemotePorts : " + ports.length);
            Log.d(TAG, "Inside Client ");

            for (String remotePort : ACTIVE_PORTS) {
                try {
                    Socket socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2, 2}), Integer.parseInt(remotePort));
                    recieversport = remotePort;
                    String msgData = msgid + "," + locseq1 + "," + senderport + "," + recieversport + "," + status + "," +"b"+ "," + msgready;

                    Log.d(TAG, "Messege sent to the server " + msgData);
                /*
                 * TODO: Fill in your client code that sends out a message.
                 */
                    BufferedWriter outclient = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));;
                    BufferedReader inclient = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    outclient.write(msgData);
                    outclient.flush();

                    String m = inclient.readLine();

                    if (m != null)
                        count++;
                    String[] outputs = m.split(",");

                    String incomingmsgid = outputs[0];
                    int propsecc = Integer.parseInt(outputs[1]);
                    String serverports = outputs[2];
                    String clientport = outputs[3];
                    status1 = Boolean.parseBoolean(outputs[4]);
                    String incomingmsg = outputs[5];


                    if (propsecc > propmax) {
                        propmax = propsecc;
                    }

                    outclient.close();
                    inclient.close();
                    socket.close();
                } catch (UnknownHostException e) {
                    Log.e(TAG, "ClientTask UnknownHostException");
                    e.printStackTrace();
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);
                } catch (IOException e) {
                    Log.e(TAG, "ClientTask socket IOException");
                    e.printStackTrace();
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);
                }
                catch(NullPointerException e){
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);

                }

            }
            if (count == ACTIVE_PORTS.size()) {
                Log.d(TAG, "maximum number ready to sent " + propmax);
                maxagreed = propmax;

            }


            String maxseqno;
            maxseqno = Integer.toString(maxagreed);

            Socket multicastsocket;

            for (String remotePort : ACTIVE_PORTS) {
                try {
                    multicastsocket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2, 2}),
                            Integer.parseInt(remotePort));

                    BufferedReader in_final = new BufferedReader(new InputStreamReader(multicastsocket.getInputStream()));
                    BufferedWriter out_final = new BufferedWriter(new OutputStreamWriter(multicastsocket.getOutputStream()));



                    String finalmsg = msgid + "," + maxseqno + "," + senderport + "," + recieversport + "," + status1 + "," + "a" + "," +msgready;
                    Log.d(TAG, "finalmsg sent " + finalmsg);
                    out_final.write(finalmsg);
                    out_final.flush();
                    if (in_final.readLine().equals("OK")){
                        out_final.close();
                        multicastsocket.close();
                    }
                    in_final.close();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);
                } catch (IOException e) {
                    e.printStackTrace();
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);
                }
                catch(NullPointerException e){
                    e.printStackTrace();
                    ACTIVE_PORTS.remove(remotePort);
                    DEAD_PORTS.add(remotePort);
                }

            }
            return null;
        }
    }

}