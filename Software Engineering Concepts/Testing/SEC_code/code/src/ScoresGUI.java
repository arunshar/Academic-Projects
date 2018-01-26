import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.border.Border;
import java.util.Random;
import java.util.*;

/**
 * This is the class that will accept the number of members
 * and creates a form with prepopulated values if scores exist.
 *
 * @author Jayashree Chandrasekaran
 * @author Sujit Singh
 * @author Harsh Nayak
 * @author Arun Sharma
 * @author Fengyu Wu
 *
 */
public class ScoresGUI implements ActionListener{

    protected JFrame frame;
    int members,iter;
    JButton submit;
    String scores[][];
    protected JComboBox[][] scoreList;
    /**
     * Create a new window containing a form.
     */
    public ScoresGUI() {

        String user_input = JOptionPane.showInputDialog(null, "Enter the number of members in the team (2-7)"); //capture the number of teammates
        if(new Members().checkUserInput(user_input) == false)
        {

            JOptionPane.showMessageDialog(null,"Please enter the valid input");
        }
        else {
            members = Integer.parseInt(user_input);


            if (new Members().checkMembers(members) == false) {
                JOptionPane.showMessageDialog(null, "Please enter the number of members between 0 and 7");
            } else {

                if (members == JOptionPane.CLOSED_OPTION)
                {
                    // Closing the dialog box if exit button is entered
                    System.exit(0);
                }

                frame = new JFrame(); // Create a window in which to display things
                JPanel panel = new JPanel();

                GridLayout gl = new GridLayout(members + 1, 4);

                panel.setLayout(gl);

                //create a dialog box with yes/No selection
                int dialogButton = JOptionPane.YES_NO_OPTION;

                int dialogResult = JOptionPane.showConfirmDialog(null, "Have you previously entered scores for your teammates? ", "Warning", dialogButton);

                //if yes is selected then create and fill scores according to number of people
                if (dialogResult == JOptionPane.YES_OPTION) {

                    // prepopulate the previous scores of the users
                    addComponents(panel, members, true);

                } else if (dialogResult == JOptionPane.NO_OPTION) {
                    // Ask the user to put new scores
                    addComponents(panel, members, false);

                } else if (dialogResult == JOptionPane.CLOSED_OPTION) {
                    System.exit(0);
                }

                frame.add(panel, BorderLayout.CENTER);
                JLabel title = new JLabel(converttoMutliLineLabel("\tOn\ta\tscale\tfrom\t0\t" +
                        "to\t5\t(0\tbeing\tthe\tlowest\tscore\tand\t5\tthe\thighest),\tevaluate\teach\tgroup\tmember’s\tperformance\tin\teach\tcategory.\t\tPlease\tbe\t" +
                        "honest\tand\tfair.\tThese\tforms\tare\tconfidential\tand\thelps\tmake\tsure\teach\tperson\tgets\tcredit\tfor,\tand\thas\ta\tgrade\treflecting,\t" +
                        "the\twork\tthey\tactually\tdid.\n" +
                        "1. The Professionalism score\tis\tfor\tshowing\tup\ton\ttime\tand\tprepared\tto\tall\twork\tsessions\tand\tmeeting,\tstaying\ton\ttask,\t\n" +
                        "treating\tall\tteammates\twith\trespect,\tand\tbehaving\tin\tan\tappropriate\tmanner.\n" +
                        "2. The\tMeeting\tParticipation score\tis\tfor\tcontributing\tto\tdiscussions\tin\tyour\tmeetings,\tcontinuing\tdiscussions\tfrom\tpast\t\n" +
                        "meetings,\tand\tcompleting\twork\talong\twith\tthe\tgroup\tduring\tthese\tmeetings.\n" +
                        "3. The\tWork\tEvaluation score\tis\tfor\tcontributing\tto the\tcompletion\tof\tthe\tproject. This\tincludes\tpreparing\tand\tediting\t\n" +
                        "documents,\treviewing\tdocuments\tcreated\tby\tothers,\tmaintaining\tyour\trepository,\thelping\tfinalize\tthe\twork\tfor\t\n" +
                        "submission,\tand\tcompleting\tany\ttasks\tassigned\tto\tthem\tbetween\tmeetings.\n"));

                submit = new JButton("submit");
                submit.addActionListener(this);

                frame.add(title, BorderLayout.NORTH);
                frame.add(submit, BorderLayout.SOUTH);// add an action listener for this and normalize on click
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Quit when frame closed
                frame.pack();
                frame.setSize(800, 800); // Set the size of the window.
                frame.setVisible(true); // Make the window visible.
            }
        }

    }

    /**
     *View the normalized scores
     *
     * @param normalizedScores Arraylist consisting of normalized scores of the user
     * @param scoreList Array of scores for each user
     * @param names String array consisting of names of each user
     *
     */
    public void viewNormalizedScores(ArrayList<Float> normalizedScores, JComboBox[][] scoreList, String[] names)
    {
        frame.setVisible(false);
        JFrame frame = new JFrame(); // Create a new window for displaying the normalized score table
        String[][] data= new String[members][5];
        // Populating the names, scores and normalized scores in the JTable
        for(int i=0;i<members;i++)
        {
            data[i][0] = names[i];
            data[i][1] = String.valueOf(scoreList[i][0].getSelectedItem());
            data[i][2] = String.valueOf(scoreList[i][1].getSelectedItem());
            data[i][3] = String.valueOf(scoreList[i][2].getSelectedItem());
            data[i][4] = String.valueOf(normalizedScores.get(i));
        }
        String column[]={"Names", "Professionalism","Meeting Participation", "Work Evaluation", "Normalized Scores"};
        JTable jt=new JTable(data,column);
        jt.setBounds(30,40,200,300);
        JScrollPane sp=new JScrollPane(jt);
        frame.add(sp);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Quit when frame closed
        frame.setSize(300,400);
        frame.setVisible(true);
    }

    /**
     *Convert single line label text to multi line text
     *
     * @param s String to convert to multi line text
     *
     * @return Returns the converted label
     */

    private String converttoMutliLineLabel(String s){
        return "<html>" + s.replaceAll("\n", "<br>");
    }


    /**
     * Create the basic frame for the scoring form.
     *
     * @param pane for adding components
     * @param members Number of members used to
     *                create the components dynamically
     * @param flag Number of members used to
     *                create the components dynamically
     */
    private void addComponents(JPanel pane, int members, boolean flag){

        //Names of the team-mates to be populated from array
        String[] names = new Members().getNames();
        String[] possible_scores = { "Select","0", "1", "2", "3", "4","5" };
        Border blackBorder =BorderFactory.createLineBorder(Color.black);

        int no_of_labels = members+4;
        JLabel [] labels = new JLabel[no_of_labels];
        scores= new String[members][3];
        labels[0] = new JLabel("Team member name");
        labels[0].setBorder(blackBorder);
        labels[1]=new JLabel("Professionalism");
        labels[1].setBorder(blackBorder);
        labels[2]= new JLabel("Meeting Participation");
        labels[2].setBorder(blackBorder);
        labels[3]= new JLabel("Work Evaluation");
        labels[3].setBorder(blackBorder);
        for (int i = 0;i<=3;i++){
            pane.add(labels[i]);
        }

        int name_ind = 0;
        Random rand = new Random();
        scoreList= new JComboBox[members][3];

        for(iter = 4;iter<no_of_labels;iter++) {
            labels[iter] = new JLabel(names[name_ind]);
            labels[iter].setBorder(blackBorder);
            name_ind++;
            pane.add(labels[iter]);
            //needs to change when extracting the text from dropdown

            for (int i=0;i<3;i++){
                scoreList[iter-4][i] = new JComboBox(possible_scores);

                // code block if true used for prepopulating scores
                if(flag == true)
                {
                    String randVal = Integer.toString(rand.nextInt(5)); // It will generate any random value from 0 to 5
                    scoreList[iter-4][i].setSelectedItem(randVal);
                }
                scoreList[iter-4][i].setSize(10,10);
                //     scoreList[iter-4].addActionListener(this);
                scoreList[iter-4][i].setBorder(blackBorder);
                pane.add(scoreList[iter-4][i]);
            }
        }
    }


    /**
     * Create the window with the framework for form
     *
     * @param args Command-line arguments which we will ignore.
     */
    public static void main(String[] args) {
        ScoresGUI gui_obj = new ScoresGUI();
    }


    /**
     * This method is declared by ActionListener. It is called whenever we click
     * on the JButton in the JFrame.
     *
     * @param e Object recording the action that caused this method to be
     *           s called.
     */

    public void actionPerformed(ActionEvent e)
    {
            String[] names = new Members().getNames();
            Scores scoreObj = new Scores();
            String[] individual_scores = new String[3];  // score of each individual of the member
            ArrayList<Float> normalizedScores = new ArrayList<Float>();
            float tempNormalizedScore = 0f;
            for(int i=0;i<members;i++)
            {
                for(int j=0;j<3;j++)
                {
                    individual_scores[j] = String.valueOf(scoreList[i][j].getSelectedItem());
                }
                tempNormalizedScore = scoreObj.normalizeScore(individual_scores,3) ;
                if(tempNormalizedScore==-1f)
                {
                    JOptionPane.showMessageDialog(null, "Please fill the complete form");
                    System.exit(0);
                }
                else
                {
                    normalizedScores.add(tempNormalizedScore);
                }
            }
        viewNormalizedScores(normalizedScores,scoreList, names);
    }
}
