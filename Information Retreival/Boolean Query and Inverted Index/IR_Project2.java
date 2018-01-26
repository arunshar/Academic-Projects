import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.PostingsEnum;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;

public class IR_Project2
{
  public static void main(String[] args)
    throws IOException
  {
    String path = args[0];
    String input_path = args[2];
    String output_path = args[1];
    
    FileSystem fs = FileSystems.getDefault();
    Path path1 = fs.getPath(path, new String[0]);
    IndexReader reader = DirectoryReader.open(FSDirectory.open(path1));
    HashMap<String, LinkedList> invertedIndex = new HashMap();
    Collection<String> fields = MultiFields.getIndexedFields(reader);
    fields.remove("_version_");
    fields.remove("id");
    TermsEnum termEnum;
    BytesRef term;
    for (Iterator localIterator = fields.iterator(); localIterator.hasNext(); (term = termEnum.next()) != null)
    {
      String content = (String)localIterator.next();
      Terms terms = MultiFields.getTerms(reader, content);
      termEnum = terms.iterator();
      
      int sum = 0;
      continue;
      BytesRef term;
      PostingsEnum iter = MultiFields.getTermDocsEnum(reader, content, term);
      LinkedList<Integer> postings_list = new LinkedList();
      String dic = term.utf8ToString();
      while (iter.nextDoc() != Integer.MAX_VALUE) {
        postings_list.add(Integer.valueOf(iter.docID()));
      }
      invertedIndex.put(dic, postings_list);
    }
    HashMap<Integer, List<String>> queries_list = new HashMap();
    try
    {
      String line = null;
      BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(input_path), "UTF-8"));
      int u1 = 0;
      while ((line = bufferedReader.readLine()) != null)
      {
        List<String> terms = new ArrayList();
        String[] tokens = line.split(" ");
        for (int i = 0; i < tokens.length; i++) {
          terms.add(tokens[i]);
        }
        queries_list.put(Integer.valueOf(u1), terms);
        u1++;
      }
      bufferedReader.close();
    }
    catch (FileNotFoundException ex)
    {
      System.out.println("Cannot open the file");
    }
    catch (IOException ex)
    {
      System.out.println("Error in reading");
    }
    BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output_path), "UTF-8"));
    for (int i = 0; i < queries_list.size(); i++)
    {
      HashMap<Integer, LinkedList> map = new HashMap();
      List<String> x = (List)queries_list.get(Integer.valueOf(i));
      for (int j = 0; j < x.size(); j++)
      {
        LinkedList<String> list1 = (LinkedList)invertedIndex.get(x.get(j));
        out.write("GetPostings");
        out.write("\n");
        out.write(((String)x.get(j)).toString());
        out.write("\n");
        out.write("Postings list: ");
        String list2 = list1.toString().replace("[", "").replace("]", "").replace(",", "");
        out.write(list2);
        out.write("\n");
        map.put(Integer.valueOf(j), list1);
      }
      LinkedList<Integer> pi = new LinkedList();
      int compute = 0;
      pi = (LinkedList)map.get(Integer.valueOf(0));
      for (int k = 0; k < map.size(); k++)
      {
        LinkedList<Integer> c = new LinkedList();
        c = (LinkedList)map.get(Integer.valueOf(k));
        LinkedList<Integer> output = new LinkedList();
        int m = 0;
        int n = 0;
        while ((m < pi.size()) && (n < c.size())) {
          if (((Integer)pi.get(m)).intValue() < ((Integer)c.get(n)).intValue())
          {
            compute++;
            m++;
          }
          else if (((Integer)pi.get(m)).intValue() == ((Integer)c.get(n)).intValue())
          {
            compute++;
            output.add((Integer)pi.get(m));
            m++;
            n++;
          }
          else if (((Integer)pi.get(m)).intValue() > ((Integer)c.get(n)).intValue())
          {
            compute++;
            n++;
          }
        }
        pi = output;
      }
      out.write("TaatAnd");
      out.write("\n");
      String list2 = x.toString().replace("[", "").replace("]", "").replace(",", "");
      String list9 = pi.toString().replace("[", "").replace("]", "").replace(",", "");
      
      out.write(list2);
      out.write("\n");
      if (pi.size() == 0)
      {
        out.write("Results: empty");
        out.write("\n");
      }
      else
      {
        out.write("Results: " + list9);
        out.write("\n");
      }
      out.write("Number of documents in results: " + pi.size());
      out.write("\n");
      
      out.write("Number of comparisons: " + compute);
      out.write("\n");
      
      LinkedList<Integer> pi1 = new LinkedList();
      int compute1 = 0;
      pi1 = (LinkedList)map.get(Integer.valueOf(0));
      for (int k = 1; k < map.size(); k++)
      {
        LinkedList<Integer> c1 = new LinkedList();
        c1 = (LinkedList)map.get(Integer.valueOf(k));
        LinkedList<Integer> output1 = new LinkedList();
        int m1 = 0;
        int n1 = 0;
        while ((m1 < pi1.size()) && (n1 < c1.size()))
        {
          if (((Integer)pi1.get(m1)).intValue() < ((Integer)c1.get(n1)).intValue())
          {
            compute1++;
            output1.add((Integer)pi1.get(m1));
            m1++;
          }
          else if (((Integer)pi1.get(m1)).intValue() == ((Integer)c1.get(n1)).intValue())
          {
            compute1++;
            output1.add((Integer)pi1.get(m1));
            m1++;
            n1++;
          }
          else if (((Integer)pi1.get(m1)).intValue() > ((Integer)c1.get(n1)).intValue())
          {
            compute1++;
            output1.add((Integer)c1.get(n1));
            n1++;
          }
          if (m1 == pi1.size()) {
            while (n1 < c1.size())
            {
              output1.add((Integer)c1.get(n1));
              n1++;
            }
          }
          if (n1 == c1.size()) {
            while (m1 < pi1.size())
            {
              output1.add((Integer)pi1.get(m1));
              m1++;
            }
          }
        }
        pi1 = output1;
      }
      out.write("TaatOr");
      out.write("\n");
      String list3 = x.toString().replace("[", "").replace("]", "").replace(",", "");
      String list8 = pi1.toString().replace("[", "").replace("]", "").replace(",", "");
      
      out.write(list3);
      out.write("\n");
      if (pi1.size() == 0)
      {
        out.write("Results: empty");
        out.write("\n");
      }
      else
      {
        out.write("Results: " + list8);
        out.write("\n");
      }
      out.write("Number of documents in results: " + pi1.size());
      out.write("\n");
      
      out.write("Number of comparisons: " + compute1);
      out.write("\n");
      
      HashMap<Integer, LinkedList> hmap = new HashMap();
      for (int i1 = 0; i1 < map.size(); i1++) {
        hmap.put(Integer.valueOf(i1), (LinkedList)map.get(Integer.valueOf(i1)));
      }
      LinkedList<Integer> id2 = new LinkedList();
      LinkedList<Integer> id3 = new LinkedList();
      int num = reader.numDocs();
      int count = 0;
      int count1 = 0;
      for (int k = 1; k <= num; k++)
      {
        for (int j = 0; j < hmap.size(); j++)
        {
          int x11;
          if (!((LinkedList)hmap.get(Integer.valueOf(j))).isEmpty())
          {
            count1++;
            x11 = ((Integer)((LinkedList)hmap.get(Integer.valueOf(j))).peek()).intValue();
            if (x11 == k)
            {
              count++;
              if (count == 1) {
                id3.add(Integer.valueOf(k));
              }
              ((LinkedList)hmap.get(Integer.valueOf(j))).remove();
            }
            else if (x11 < k)
            {
              id3.add(Integer.valueOf(k));
              ((LinkedList)hmap.get(Integer.valueOf(j))).remove();
            }
          }
          else
          {
            x11 = 1;
          }
        }
        if (count == hmap.size()) {
          id2.add(Integer.valueOf(k));
        }
        count = 0;
        j = 0;
      }
      out.write("DaatAnd");
      out.write("\n");
      String list4 = x.toString().replace("[", "").replace("]", "").replace(",", "");
      String list7 = id2.toString().replace("[", "").replace("]", "").replace(",", "");
      
      out.write(list4);
      out.write("\n");
      if (id2.size() == 0)
      {
        out.write("Results: empty");
        out.write("\n");
      }
      else
      {
        out.write("Results: " + list7);
        out.write("\n");
      }
      out.write("Number of documents in results: " + id2.size());
      out.write("\n");
      
      out.write("Number of comparisons: " + count1++);
      out.write("\n");
      
      out.write("DaatOr");
      out.write("\n");
      String list5 = x.toString().replace("[", "").replace("]", "").replace(",", "");
      String list6 = id3.toString().replace("[", "").replace("]", "").replace(",", "");
      
      out.write(list5);
      out.write("\n");
      if (id3.size() == 0)
      {
        out.write("Results: empty");
        out.write("\n");
      }
      else
      {
        out.write("Results: " + list6);
        out.write("\n");
      }
      out.write("Number of documents in results: " + id3.size());
      out.write("\n");
      
      out.write("Number of comparisons: " + count1++);
      out.write("\n");
    }
    out.close();
  }
}
