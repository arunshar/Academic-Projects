package edu.buffalo.cse.cse486586.simpledht;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Formatter;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.database.MergeCursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.provider.BaseColumns;
import android.telephony.TelephonyManager;
import android.util.Log;

public class SimpleDhtProvider extends ContentProvider {
    String myPort;
    String nextPort;
    String prevPort;
    String myId;
    String nextId;
    String prevId;
    String MASTER_PORT = "5554";
    FeedReaderDbHelper helper;
    String waitingForMessage = "waiting";
    MergeCursor globalCursor;
    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        if(selection.equals("*") || selection.equals("@")){
            SQLiteDatabase db = helper.getWritableDatabase();
            db.execSQL("DELETE FROM entry;");
            if(selection.equals("*")){
                String message = myPort+"|DELETE|"+selection;
                clientTask(message, nextPort);
            }
        }
        else{
            if(check(selection)){
                SQLiteDatabase db = helper.getWritableDatabase();
                db.delete("entry", "key=?", new String[]{selection});
                return 0;
            }
            String message = myPort+"|DELETE|"+selection;
            clientTask(message, nextPort);
        }
        return 0;
    }

    @Override
    public String getType(Uri uri) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        if(check(values.getAsString("key"))){
            SQLiteDatabase db = helper.getWritableDatabase();
            long entry = db.insertWithOnConflict("entry", null, values, SQLiteDatabase.CONFLICT_REPLACE);
            Log.d("CP_INSERTED", ""+entry);
        }
        else{
            String message = myPort + "|INSERT|" + values.getAsString("key") + "|" + values.getAsString("value");
            clientTask(message, nextPort);
        }
        return null;
    }

    @Override
    public boolean onCreate() {
        try{
            TelephonyManager tel = (TelephonyManager) getContext().getSystemService(this.getContext().TELEPHONY_SERVICE);
            myPort = tel.getLine1Number().substring(tel.getLine1Number().length() - 4);
            nextPort = myPort;
            prevPort = myPort;
            myId = genHash(myPort);
            nextId = myId;
            prevId = myId;
            helper = new FeedReaderDbHelper(getContext());
            ServerSocket serverSocket = new ServerSocket(10000);
            serverTask(serverSocket);

            //Creating join message
            // MY_PORT | MESSAGE_TYPE
            if(!myPort.equals(MASTER_PORT)){
                String message = myPort + "|" + "JOIN";
                clientTask(message, MASTER_PORT);
            }
        }
        catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
            Log.d("ON_CREATE", "ERROR CREATING SOCKET");
        }

        return false;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
            String sortOrder) {
        if(selection.equals("*") || selection.equals("@")){
            SQLiteDatabase db = helper.getWritableDatabase();
            Cursor cursor = db.rawQuery("SELECT * FROM entry;",null);
            globalCursor = new MergeCursor(new Cursor[]{cursor});
            Log.d(selection+ " Query :", ""+cursor.getCount());
            if(selection.equals("*")){
                String tempValue = "";
                if(cursor.moveToFirst()){
                    while(cursor.isAfterLast()==false){
                        tempValue += cursor.getString(cursor.getColumnIndex("key")) + "," + cursor.getString(cursor.getColumnIndex("value")) + "+";
                        cursor.moveToNext();
                    }
                }
                String message = myPort + "|QUERY_MULTIPLE|" + selection + "|" + tempValue;
                clientTask(message, nextPort);
                synchronized (waitingForMessage){
                    try {
                        waitingForMessage.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
            return globalCursor;
        }
        else if (check(selection)){
            SQLiteDatabase db = helper.getWritableDatabase();
            Cursor cursor = db.query("entry", null, "key=?", new String[] {selection}, null, null, null);
            return cursor;
        }
        else{
            String message = myPort + "|QUERY_SINGLE|" + selection;
            clientTask(message, nextPort);
            try {
                synchronized (waitingForMessage){
                    waitingForMessage.wait();
                }
                return globalCursor;
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        // TODO Auto-generated method stub
        return 0;
    }

    private String genHash(String input) throws NoSuchAlgorithmException {
        MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        byte[] sha1Hash = sha1.digest(input.getBytes());
        Formatter formatter = new Formatter();
        for (byte b : sha1Hash) {
            formatter.format("%02x", b);
        }
        return formatter.toString();
    }

    private void clientTask(final String message, final String remotePort){
        new Thread(new Runnable() {
            @Override
            public void run() {
                try{
                    Socket socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(remotePort)*2);
                    DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                    out.writeUTF(message);
                    out.flush();
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                    Log.d("Client Task :","UnknownHostException Error sending  - "+message);
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.d("Client Task :","IOException Error sending  - "+message);
                }

            }
        }).start();
    }
    private void serverTask(final ServerSocket serverSocket){
        new Thread(new Runnable() {
            @Override
            public void run() {
                while(true){
                    try{
                        Socket socket = serverSocket.accept();
                        DataInputStream reader= new DataInputStream(socket.getInputStream());
                        String message = reader.readUTF();
                        if(message!=null){
                            Log.d("SERVER :", "MESSAGE RECEIVED - "+message);
                            String data[] = message.split("\\|");
                            if(data[1].equals("JOIN")){
                                if(check(data[0])){
                                    //JOIN REPLY
                                    //MESSAGE = MY_PORT | MESSAGE_TYPE | PREV_PORT
                                    String joinReply = myPort + "|JOIN_REPLY|" + prevPort;
                                    if(myPort.equals(nextPort)){
                                        prevPort = data[0];
                                        nextPort = data[0];
                                        nextId = genHash(nextPort);
                                        prevId = genHash(prevPort);
                                    }
                                    else{
                                        prevPort = data[0];
                                        prevId = genHash(prevPort);
                                    }
                                    //SEND REPLY TO SENDER
                                    clientTask(joinReply, data[0]);
                                }
                                else{
                                    //Forward the message to next node in ring
                                    clientTask(message, nextPort);
                                }
                            }
                            else if(data[1].equals("JOIN_REPLY")){
                                nextPort = data[0];
                                prevPort = data[2];
                                nextId = genHash(nextPort);
                                prevId = genHash(prevPort);
                                Log.d(myPort + " UPDATED NEXT :", nextPort);
                                Log.d(myPort + " UPDATED PREV :", prevPort);
                                //Update next message
                                String updateNext = myPort + "|UPDATE_NEXT";
                                clientTask(updateNext, prevPort);
                            }
                            else if(data[1].equals("UPDATE_NEXT")){
                                nextPort = data[0];
                                nextId = genHash(nextPort);
                                Log.d(myPort + " UPDATED NEXT :", nextPort);
                            }
                            else if(data[1].equals("INSERT")){
                                if(check(data[2])){
                                    ContentValues values = new ContentValues();
                                    values.put("key", data[2]);
                                    values.put("value", data[3]);
                                    SQLiteDatabase db = helper.getWritableDatabase();
                                    db.insertWithOnConflict("entry", null, values, SQLiteDatabase.CONFLICT_REPLACE);
                                }
                                else{
                                    clientTask(message, nextPort);
                                }
                            }
                            else if(data[1].equals("QUERY_SINGLE")){
                                //MESSAGE = ORGINATING_PORT | MESSAGE_TYPE | KEY
                                if(check(data[2])){
                                    SQLiteDatabase db = helper.getWritableDatabase();
                                    Cursor cursor = db.query("entry", null, "key=?", new String[]{data[2]}, null, null, null);
                                    cursor.moveToFirst();
                                    String msgtosend = myPort+"|QUERY_REPLY_SINGLE|"+data[2]+","+cursor.getString(cursor.getColumnIndex("value"));
                                    clientTask(msgtosend,data[0]);
                                } else {
                                    clientTask(message,nextPort);
                                }
                            }
                            else if(data[1].equals("QUERY_REPLY_SINGLE")){
                                String response[] = data[2].split(",");
                                MatrixCursor tempCursor = new MatrixCursor(new String[]{"key","value"});
                                tempCursor.addRow(response);
                                globalCursor = new MergeCursor(new Cursor[]{tempCursor});
                                synchronized (waitingForMessage){
                                    waitingForMessage.notify();
                                }
                            }
                            else if(data[1].equals("QUERY_MULTIPLE")){
                                if(data[0].equals(myPort)){
                                    MatrixCursor tempCursor = new MatrixCursor(new String[]{"key","value"});
                                    if(data.length>3){
                                        String rows[] = data[3].split("\\+");
                                        for(String row : rows){
                                            if(row!=null && row.length()>0){
                                                String dataFrame[] = row.split("\\,");
                                                tempCursor.addRow(dataFrame);
                                            }
                                        }
                                    }
                                    globalCursor = new MergeCursor(new Cursor[]{tempCursor});
                                    synchronized (waitingForMessage){
                                        waitingForMessage.notify();
                                    }
                                }
                                else{
                                    SQLiteDatabase db = helper.getWritableDatabase();
                                    Cursor cursor = db.rawQuery("SELECT * FROM entry;",null);
                                    String tempValue = "";
                                    while(cursor.moveToNext()){
                                        tempValue += cursor.getString(cursor.getColumnIndex("key")) + "," + cursor.getString(cursor.getColumnIndex("value")) + "+";
                                    }
                                    message = message + tempValue;
                                    clientTask(message, nextPort);
                                }
                            }
                            else if(data[1].equals("DELETE")){
                                if(data[0].equals(myPort)) {
                                    if(data[2].equals("*")){
                                        SQLiteDatabase db = helper.getWritableDatabase();
                                        db.execSQL("DELETE FROM entry;");
                                        clientTask(message,nextPort);
                                    }
                                    else{
                                        if(check(data[2])){
                                            SQLiteDatabase db = helper.getWritableDatabase();
                                            db.delete("entry", "key=?", new String[]{data[2]});
                                        }
                                        else{
                                            clientTask(message,nextPort);
                                        }
                                    }
                                }
                            }
                        }
                    }
                    catch (IOException e) {
                        e.printStackTrace();
                    } catch (NoSuchAlgorithmException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    private boolean check(String check){
        try{
            String checkId = genHash(check);
            if(myPort.equals(nextPort)){
                return true;
            }
            if(myId.compareTo(prevId)<0){
                if((checkId.compareTo(myId)<0) && (checkId.compareTo(prevId)<0)){
                    return true;
                }
                if(checkId.compareTo(myId)>0 && checkId.compareTo(prevId)>0){
                    return true;
                }
            }
            else if(checkId.compareTo(prevId)>0 && checkId.compareTo(myId)<=0){
                return true;
            }
            return false;
        }
        catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return false;
        }
    }

    /**
     * DATABASE SHIT DO NOT TOUCH
     * */
    public class DatabaseEntry implements BaseColumns {
        public static final String TABLE_NAME = "entry";
        public static final String KEY_FIELD = "key";
        public static final String VALUE_FIELD = "value";
    }

    public class FeedReaderDbHelper extends SQLiteOpenHelper {
        public static final String SQL_CREATE_ENTRIES =
                "CREATE TABLE IF NOT EXISTS " + "entry" + " (" +
                        "key" + " TEXT PRIMARY KEY, " +
                        "value" + " TEXT)";
        public static final int DATABASE_VERSION = 1;
        public static final String DATABASE_NAME = "FeedReader.db";

        public FeedReaderDbHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db) {

            db.execSQL(SQL_CREATE_ENTRIES);

        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            onCreate(db);
        }
    }
}
