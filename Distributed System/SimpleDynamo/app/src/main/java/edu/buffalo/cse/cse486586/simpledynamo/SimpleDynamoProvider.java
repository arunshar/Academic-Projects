package edu.buffalo.cse.cse486586.simpledynamo;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Formatter;
import java.util.Timer;
import java.util.concurrent.CopyOnWriteArrayList;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.CursorIndexOutOfBoundsException;
import android.database.MatrixCursor;
import android.database.MergeCursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.provider.BaseColumns;
import android.telephony.TelephonyManager;
import android.util.Log;
import java.util.Timer;
import java.util.concurrent.TimeoutException;

import static android.content.ContentValues.TAG;

public class SimpleDynamoProvider extends ContentProvider {
	CopyOnWriteArrayList<String> ACTIVE_PORTS = new CopyOnWriteArrayList<String>();
	CopyOnWriteArrayList<String> DEAD_PORTS = new CopyOnWriteArrayList<String>();
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
	static final String[] REMOTE_PORT = {"11124","11112","11108","11116","11120"};
	static final String[] Nodes= {"5562","5556","5554","5558","5560"};
	static final int SERVER_PORT = 10000;
	@Override
	public int delete(Uri uri, String selection, String[] selectionArgs) {
//		if(selection.equals("*") || selection.equals("@")){
//			SQLiteDatabase db = helper.getWritableDatabase();
//			db.execSQL("DELETE FROM entry;");
//			if(selection.equals("*")){
//				String message = myPort+"|DELETE|"+selection;
//				clientTask(message, nextPort);
//			}
//		}
//		else{
		String destnode = check(selection);

		if(destnode.equals(myPort)){

			String nodesuc1 = SuccessorOne(myPort);
			String nodesuc2 = SuccessorTwo(myPort);
			SQLiteDatabase db = helper.getWritableDatabase();
			db.delete("entry", "key=?", new String[]{selection});
			String message = myPort+"|DELETE|"+selection + "|" + destnode;
			clientTask(message,nodesuc1);
			clientTask(message,nodesuc2);
		}
		else {
			String message = myPort+"|DELETE|"+selection + "|" + destnode;

			String nodesuc1 = SuccessorOne(destnode);
			String nodesuc2 = SuccessorTwo(destnode);
			clientTask(message, destnode);
			clientTask(message,nodesuc1);
			clientTask(message,nodesuc2);
		}
		return 0;
	}

	@Override
	public String getType(Uri uri) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public synchronized Uri insert(Uri uri, ContentValues values) {

//		for (String port : Nodes){
//			String ack = myPort+"|"+"ACK"+"|"+port;
//			clientTask(ack,port);
//		}
//		try {
//			Thread.sleep(100);
//		} catch (InterruptedException e) {
//			e.printStackTrace();
//		}
		Log.d(TAG, "Active ports after insertion : " + ACTIVE_PORTS);
		String key = values.getAsString("key");
		String destnode = check(key);
		Log.e(TAG, "destination node : "+destnode);
		if(destnode.equals(myPort)){
			SQLiteDatabase db = helper.getWritableDatabase();
			long entry = db.insertWithOnConflict("entry", null, values, SQLiteDatabase.CONFLICT_REPLACE);
			Log.d("CP_INSERTED", ""+entry);

			String nodesuc1 = SuccessorOne(myPort);
			String nodesuc2 = SuccessorTwo(myPort);
			String message = myPort + "|INSERT|" + values.getAsString("key") + "|" + values.getAsString("value") + "|" + destnode;
			clientTask1(message,nodesuc1);
			clientTask1(message,nodesuc2);
		}
		else{

			String nodesuc1 = SuccessorOne(destnode);
			String nodesuc2 = SuccessorTwo(destnode);
			String message = myPort + "|INSERT|" + values.getAsString("key") + "|" + values.getAsString("value") + "|" + destnode;
			clientTask1(message, destnode);
			clientTask1(message, nodesuc1);
			clientTask1(message, nodesuc2);
		}
		return null;
	}

	@Override
	public boolean onCreate() {
		try{
			TelephonyManager tel = (TelephonyManager) getContext().getSystemService(this.getContext().TELEPHONY_SERVICE);
			myPort = tel.getLine1Number().substring(tel.getLine1Number().length() - 4);
//			nextPort = myPort;
//			prevPort = myPort;
//			myId = genHash(myPort);
//			nextId = myId;
//			prevId = myId;
//			for (String port : Nodes){
//				ACTIVE_PORTS.add(port);
//			}

			helper = new FeedReaderDbHelper(getContext());
			ServerSocket serverSocket = new ServerSocket(10000);
			serverTask(serverSocket);

//			//Creating join message
//			// MY_PORT | MESSAGE_TYPE
//			if(!myPort.equals(MASTER_PORT)){
//				String message = myPort + "|" + "JOIN";
//				clientTask(message, MASTER_PORT);
//			}
			SQLiteDatabase db = helper.getWritableDatabase();
			Cursor cursor = db.rawQuery("SELECT * FROM entry;",null);
			if(cursor != null && cursor.getCount() > 0){
				db.execSQL("DELETE FROM entry;");
				String nodepred1 = PredecessorOne(myPort);
				String nodepred2 = PredecessorTwo(myPort);

				String nodesuc1 = SuccessorOne(myPort);
				String nodesuc2 = SuccessorTwo(myPort);
				String message = myPort + "|RECOVERY|" + nodepred1 + "|" + nodepred2;
				clientTask1(message,nodepred1);
				clientTask1(message,nodepred2);
				clientTask1(message,nodesuc1);
				clientTask1(message,nodesuc2);
			}

		}


		catch (IOException e) {
			e.printStackTrace();
			Log.d("ON_CREATE", "ERROR CREATING SOCKET");
		}


		return false;
	}

	@Override
	public synchronized Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
									 String sortOrder) {
		Log.d(TAG, "Active ports after insertion : " + ACTIVE_PORTS);
		String destnode = check(selection);

		String nodesuc1 = SuccessorOne(destnode);
		String nodesuc2 = SuccessorTwo(destnode);
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
//                for(String port : REMOTE_PORT){
//                    clientTask(message,port);
//                }

				String nextport = SuccessorOne(myPort);
				clientTask(message, nextport);

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
		else if (destnode.equals(myPort)){
			SQLiteDatabase db = helper.getWritableDatabase();
			Cursor cursor = db.query("entry", null, "key=?", new String[] {selection}, null, null, null);
			return cursor;
		}
		else{
			int count = 0;
			String message = myPort + "|QUERY_SINGLE|" + selection + "|" + destnode + "|" + nodesuc1 + "|" + nodesuc2;
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			clientTask(message, destnode);

			try {
				synchronized (waitingForMessage){
					waitingForMessage.wait();
				}
				return globalCursor;

			} catch (InterruptedException e) {
				e.printStackTrace();
			}


//			for(int i =0;i < 5;i++){
//				try {
//					Thread.sleep(1000);
//				} catch (InterruptedException e) {
//					e.printStackTrace();
//				}
//				count++;
//				if(count>3){
//					clientTask(message,nodesuc1);
//					Log.e(TAG, "Here comes the second : "+nodesuc1);
//					synchronized (waitingForMessage){
//						try {
//							waitingForMessage.wait();
//						} catch (InterruptedException e) {
//							e.printStackTrace();
//						}
//						return globalCursor;
//					}
//				}
//			}


//			clientTask(message, nodesuc1);
//            clientTask(message, nodesuc2);

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
					Log.e("Client_Task_called","");
					Socket socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(remotePort)*2);
					DataOutputStream out = new DataOutputStream(socket.getOutputStream());
					DataInputStream in = new DataInputStream(socket.getInputStream());
					out.writeUTF(message);
					out.flush();
					if (in.readUTF().equals("OK")){
						out.close();
						socket.close();
					}
				} catch (UnknownHostException e) {
					e.printStackTrace();
					Log.d("Client Task :","UnknownHostException Error sending  - "+message);
				} catch (EOFException e){
					Socket socket = null;
					try {
//
						String nodesuc1 = SuccessorOne(remotePort);
						socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(nodesuc1)*2);
						DataOutputStream out = new DataOutputStream(socket.getOutputStream());
						DataInputStream in = new DataInputStream(socket.getInputStream());
						out.writeUTF(message);
						out.flush();
						if (in.readUTF().equals("OK")){
							out.close();
							socket.close();
						}
					} catch (IOException e1) {
						e1.printStackTrace();
					}
				} catch (IOException e) {
					Socket socket = null;
					try {

//
						String nodesuc1 = SuccessorOne(remotePort);
						socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(nodesuc1)*2);
						DataOutputStream out = new DataOutputStream(socket.getOutputStream());
						DataInputStream in = new DataInputStream(socket.getInputStream());
						out.writeUTF(message);
						out.flush();
						if (in.readUTF().equals("OK")){
							out.close();
							socket.close();
						}
					} catch (IOException e1) {
						e1.printStackTrace();
					}
					Log.d("Client Task :","IOException Error sending  - "+message);
				}  catch (NullPointerException e){
					e.printStackTrace();
					Log.d(TAG, "Null pointer exception");
				}
			}
		}).start();
	}

	private void clientTask1(final String message, final String remotePort){
		new Thread(new Runnable() {
			@Override
			public void run() {
				try{
					Log.e("Client_Task_called","");
					Socket socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(remotePort)*2);
					DataOutputStream out = new DataOutputStream(socket.getOutputStream());
					DataInputStream in = new DataInputStream(socket.getInputStream());
					out.writeUTF(message);
					out.flush();
					if (in.readUTF().equals("OK")){
						out.close();
						socket.close();
					}
				} catch (UnknownHostException e) {
					e.printStackTrace();
					Log.d("Client Task :","UnknownHostException Error sending  - "+message);
				} catch (EOFException e){
//					Socket socket = null;
//					try {
//						int index= Arrays.asList(Nodes).indexOf(remotePort);
//						String nodesuc1 = Nodes[(index+1)%5];
//						socket = new Socket(InetAddress.getByAddress(new byte[]{10, 0, 2 ,2}), Integer.parseInt(nodesuc1)*2);
//						DataOutputStream out = new DataOutputStream(socket.getOutputStream());
//						DataInputStream in = new DataInputStream(socket.getInputStream());
//						out.writeUTF(message);
//						out.flush();
//						if (in.readUTF().equals("OK")){
//							out.close();
//							socket.close();
//						}
//					} catch (IOException e1) {
//						e1.printStackTrace();
//					}
				} catch (IOException e) {
					e.printStackTrace();
					Log.d("Client Task :","IOException Error sending  - "+message);
				}  catch (NullPointerException e){
					e.printStackTrace();
					Log.d(TAG, "Null pointer exception");
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
						DataOutputStream writer = new DataOutputStream(socket.getOutputStream());
						String message = reader.readUTF();
						writer.writeUTF("OK");
						writer.flush();
						if(message!=null){
							Log.d("SERVER :", "MESSAGE RECEIVED - "+message);
							String data[] = message.split("\\|");
//							if(data[1].equals("ACK")){
//								Log.e(TAG, "I AM ALIVE");
//							}
							if(data[1].equals("INSERT")){
								Log.e("Insert_Task_called","");
								ContentValues values = new ContentValues();
								values.put("key", data[2]);
								values.put("value", data[3]);
								SQLiteDatabase db = helper.getWritableDatabase();
								db.insertWithOnConflict("entry", null, values, SQLiteDatabase.CONFLICT_REPLACE);
							}
							else if(data[1].equals("RECOVERY")){
								String sendersport = data[0];
								SQLiteDatabase db = helper.getWritableDatabase();
								Cursor cursor = db.rawQuery("SELECT * FROM entry;",null);
								String tempValue = "";
								if(cursor.moveToFirst()){
									while(cursor.isAfterLast()==false){
										String coordinator = check(cursor.getString(cursor.getColumnIndex("key")));
										if(coordinator.equals(sendersport) || coordinator.equals((PredecessorOne(sendersport))) || coordinator.equals(PredecessorTwo(sendersport))){
											tempValue += cursor.getString(cursor.getColumnIndex("key")) + "," + cursor.getString(cursor.getColumnIndex("value")) + "+";
										}
										//tempValue += cursor.getString(cursor.getColumnIndex("key")) + "," + cursor.getString(cursor.getColumnIndex("value")) + "+";
										cursor.moveToNext();

									}
								}
								if (!tempValue.isEmpty()){
									message = myPort + "|UPDATE|" + sendersport + "|" + tempValue;
									clientTask(message,sendersport);
								}
							}
							else if(data[1].equals("UPDATE")){
								if (data.length >= 3 || data[3]!= null) {
									String rows[] = data[3].split("\\+");
									for(String row : rows){
										if(row!=null && row.length() > 0){
											String dataFrame[] = row.split("\\,");
											ContentValues values = new ContentValues();
											values.put("key", dataFrame[0]);
											values.put("value", dataFrame[1]);
											SQLiteDatabase db = helper.getWritableDatabase();
											db.insertWithOnConflict("entry", null, values, SQLiteDatabase.CONFLICT_REPLACE);
										}
									}

								}
							}
							else if(data[1].equals("QUERY_SINGLE")){
								SQLiteDatabase db = helper.getWritableDatabase();
								Log.e(TAG, "key : "+data[2]);
								Cursor cursor = db.query("entry", null, "key=?", new String[]{data[2]}, null, null, null);
									try{
										if(cursor != null || cursor.getCount() > 0) {
											cursor.moveToFirst();
//											String val1 = cursor.getString(cursor.getColumnIndex("value"));
											Log.e(TAG, "key : " + data[2] + "value : " + cursor.getString(cursor.getColumnIndex("value")));
											String msgtosend = myPort + "|QUERY_REPLY_SINGLE|" + data[2] + "," + cursor.getString(cursor.getColumnIndex("value"));
											clientTask(msgtosend, data[0]);
										}
									} catch (CursorIndexOutOfBoundsException e){
										String nextport = SuccessorOne(myPort);
										clientTask(message,nextport);
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
//
									String nextport = SuccessorOne(myPort);
									clientTask(message, nextport);
//									clientTask(message, nextPort);
								}
							}
							else if(data[1].equals("DELETE")){
								SQLiteDatabase db = helper.getWritableDatabase();
								db.delete("entry", "key=?", new String[]{data[2]});
							}
						}
					}
					catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
		}).start();
	}



	private String check(String key){
		try {

			String hashkey = genHash(key);

			if(genHash(Nodes[0]).compareTo(hashkey) >=0 || genHash(Nodes[4]).compareTo(hashkey)<0){
				return Nodes[0];
			}else if(genHash(Nodes[1]).compareTo(hashkey)>=0 && genHash(Nodes[0]).compareTo(hashkey)<0 ){
				return Nodes[1];
			}else if(genHash(Nodes[2]).compareTo(hashkey)>=0 && genHash(Nodes[1]).compareTo(hashkey)<0 ){
				return Nodes[2];
			}else if(genHash(Nodes[3]).compareTo(hashkey)>=0 && genHash(Nodes[2]).compareTo(hashkey)<0 ){
				return Nodes[3];
			}else if(genHash(Nodes[4]).compareTo(hashkey)>=0 && genHash(Nodes[3]).compareTo(hashkey)<0 ){
				return Nodes[4];
			}

		}catch(Exception e){
			e.printStackTrace();
		}

		return null;
	}

	private String SuccessorOne(String node){
		if(node.equals("5562")){
			return "5556";
		}else if(node.equals("5556")){
			return "5554";
		} else if(node.equals("5554")){
			return "5558";
		} else if(node.equals("5558")){
			return "5560";
		}else if(node.equals("5560")){
			return "5562";
		}
		return null;
	}

	private String SuccessorTwo(String node){
		if(node.equals("5562")){
			return "5554";
		}else if(node.equals("5556")){
			return "5558";
		} else if(node.equals("5554")){
			return "5560";
		} else if(node.equals("5558")){
			return "5562";
		}else if(node.equals("5560")){
			return "5556";
		}
		return null;
	}

	private String PredecessorOne(String node){
		if(node.equals("5562")){
			return "5560";
		}else if(node.equals("5556")){
			return "5562";
		} else if(node.equals("5554")){
			return "5556";
		} else if(node.equals("5558")){
			return "5554";
		}else if(node.equals("5560")){
			return "5558";
		}
		return null;
	}

	private String PredecessorTwo(String node){
		if(node.equals("5562")){
			return "5558";
		}else if(node.equals("5556")){
			return "5560";
		} else if(node.equals("5554")){
			return "5562";
		} else if(node.equals("5558")){
			return "5556";
		}else if(node.equals("5560")){
			return "5554";
		}
		return null;
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
