import static org.junit.Assert.*;
import org.junit.Test;

/**
 * Test cases for ScoresGUI
 * @author Jayashree Chandrasekaran
 * @author Sujit Singh
 * @author Harsh Nayak
 * @author Arun Sharma
 * @author Fengyu Wu
 */
public class ScoresGUITest {
    @SuppressWarnings("deprecation")
    @Test
    /**
     *  Evaluates test case for Normalizing scores
     */
    public void testNormalizeScores() {
        Scores scoreObj = new Scores();
        String[] x = new String[5];
        x[0] = "Select";
        x[1] = "Select";
        x[2] = "Select";
        float actual = scoreObj.normalizeScore(x, 5);
        float expected = -1f;
        assertEquals(expected, actual, 0.0001);
    }

    @Test
    /**
     *  Evaluates test cases for checking the number of members
     */
    public void testCheckMembers() {
        Members guiObj = new Members();
        int trueMember = 5;
        int upperBoundMembers = 8;
        int lowerBoundMembers = 1;
        int negMembers = -1;
        assertEquals(true,guiObj.checkMembers(trueMember)) ;
        assertEquals(false,guiObj.checkMembers(upperBoundMembers)) ;
        assertEquals(false,guiObj.checkMembers(lowerBoundMembers)) ;
        assertEquals(false,guiObj.checkMembers(negMembers)) ;
    }

    @Test
    /**
     *  Evalutes empty & invalid input in the input member stage
     */
    public void testUserInput()
    {
        Members guiObj = new Members();
        String testInput1 = "";
        String testInput2 = "5";
        String testInput3 = "j;lasjfjsfj;jjf@@#$#%$^&*(";
        assertEquals(false, guiObj.checkUserInput(testInput1));
        assertEquals(true,guiObj.checkUserInput(testInput2));
        assertEquals(false,guiObj.checkUserInput(testInput3));
    }
}
