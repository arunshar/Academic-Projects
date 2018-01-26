package edu.buffalo.cse.cse486586.groupmessenger1;

import android.content.ContentProvider;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.BaseColumns;
import android.provider.UserDictionary;
import android.util.Log;
import android.database.sqlite.*;

//import static android.R.attr.key;
//import static android.R.attr.value;
import static android.R.attr.key;
import static android.database.sqlite.SQLiteDatabase.CONFLICT_REPLACE;
//import static edu.buffalo.cse.cse486586.groupmessenger1.Database.DatabaseEntry.TABLE_NAME;
//import static edu.buffalo.cse.cse486586.groupmessenger1.GroupMessengerProvider.DatabaseEntry.TABLE_NAME;
import static edu.buffalo.cse.cse486586.groupmessenger1.GroupMessengerProvider.DatabaseEntry.TABLE_NAME;
import static edu.buffalo.cse.cse486586.groupmessenger1.OnPTestClickListener.KEY_FIELD;
import static edu.buffalo.cse.cse486586.groupmessenger1.OnPTestClickListener.VALUE_FIELD;
import static java.security.AccessController.getContext;
import java.security.AccessControlContext;
import java.util.Arrays;
//import edu.buffalo.cse.cse486586.groupmessenger1.Database.DatabaseEntry;

//import static edu.buffalo.cse.cse486586.groupmessenger1.Database.DatabaseEntry.*;


/**
 * GroupMessengerProvider is a key-value table. Once again, please note that we do not implement
 * full support for SQL as a usual ContentProvider does. We re-purpose ContentProvider's interface
 * to use it as a key-value table.
 * 
 * Please read:
 * 
 * http://developer.android.com/guide/topics/providers/content-providers.html
 * http://developer.android.com/reference/android/content/ContentProvider.html
 * 
 * before you start to get yourself familiarized with ContentProvider.
 * 
 * There are two methods you need to implement---insert() and query(). Others are optional and
 * will not be tested.
 * 
 * @author stevko
 *
 */

/**
 * For making SQL Database with SQLlite, the following code snippet is taken from
 * https://developer.android.com/training/basics/data-storage/databases.html
 * For simplicity I've used exactly the same variables as they used in the documentation.
 */

public class GroupMessengerProvider extends ContentProvider {
    FeedReaderDbHelper helper;

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        // You do not need to implement this.
        return 0;
    }

    @Override
    public String getType(Uri uri) {
        // You do not need to implement this.
        return null;
    }

    public class DatabaseEntry implements BaseColumns {
        public static final String TABLE_NAME = "entry";
        public static final String KEY_FIELD = "key";
        public static final String VALUE_FIELD = "value";
    }
    public static final String SQL_CREATE_ENTRIES =
            "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " (" +
                    DatabaseEntry.KEY_FIELD + " TEXT PRIMARY KEY, " +
                    DatabaseEntry.VALUE_FIELD+ " TEXT)";



    public class FeedReaderDbHelper extends SQLiteOpenHelper {
        public static final int DATABASE_VERSION = 1;
        public static final String DATABASE_NAME = "FeedReader.db";

        public FeedReaderDbHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);

        }

        public void onCreate(SQLiteDatabase db) {
            db.execSQL(SQL_CREATE_ENTRIES);
        }

        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            onCreate(db);

        }

    }
    //FeedReaderDbHelper helper = new FeedReaderDbHelper(getContext());
    //SQLiteDatabase db = helper.getWritableDatabase();
    //ContentValues values = new ContentValues();
    //db.execSQL("DROP TABLE groupmessenger;")

    @Override
    public Uri insert(Uri uri, ContentValues values) {

        //Insert;
        SQLiteDatabase db = helper.getWritableDatabase();
        long newRowId = db.insertWithOnConflict("entry", null, values, CONFLICT_REPLACE);


        // Defines a new Uri object that receives the result of the insertion
// Defines an object to contain the new values to insert

//
        //* Sets the values of each column and inserts the word. The arguments to the "put"
        //* method are "column name" and "value"


        /*
         * TODO: You need to implement this method. Note that values will have two columns (a key
         * column and a value column) and one row that contains the actual (key, value) pair to be
         * inserted.
         * 
         * For actual storage, you can use any option. If you know how to use SQL, then you can use
         * SQLite. But this is not a requirement. You can use other storage options, such as the
         * internal storage option that we used in PA1. If you want to use that option, please
         * take a look at the code for PA1.
         */
        Log.v("insert", values.toString());
        return uri;
    }


    @Override
    public boolean onCreate() {
        // If you need to perform any one-time initialization task, please do it here.
        helper = new FeedReaderDbHelper(getContext());
        return false;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        // You do not need to implement this.
        return 0;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
                        String sortOrder) {



        SQLiteDatabase db = helper.getWritableDatabase();
        SQLiteQueryBuilder qbuilder = new SQLiteQueryBuilder();
        qbuilder.setTables("entry");
        Cursor cursor = qbuilder.query(
                db,                     // The table to query
                projection,                               // The columns to return
                "key=?",                                // The columns for the WHERE clause
                new String[] {selection},                            // The values for the WHERE clause
                null,                                     // don't group the rows
                null,                                     // don't filter by row groups
                sortOrder                                 // The sort order
        );
        /*
         * TODO: You need to implement this method. Note that you need to return a Cursor object
         * with the right format. If the formatting is not correct, then it is not going to work.
         *
         * If you use SQLite, whatever is returned from SQLite is a Cursor object. However, you
         * still need to be careful because the formatting might still be incorrect.
         *
         * If you use a file storage option, then it is your job to build a Cursor * object. I
         * recommend building a MatrixCursor described at:
         * http://developer.android.com/reference/android/database/MatrixCursor.html
         */
        Log.v("query", selection + cursor.getColumnName(0));
        return cursor;
    }


}
