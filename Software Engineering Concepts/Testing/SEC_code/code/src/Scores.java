import java.util.*;
/**
 * Score class for handling the operations for normalization
 * @author Jayashree Chandrasekaran
 * @author Sujit Singh
 * @author Harsh Nayak
 * @author Arun Sharma
 * @author Fengyu Wu
 */
public class Scores {

    /**
     * Normalizes score given by the members
     *
     * @param scores String array consisting of scores of each member
     * @param maxValue the maximum possible score that can be given to a member
     * @return float value of the normalized score of each user
     */
    public float normalizeScore(String[] scores, int maxValue)
    {
        try
        {
            Integer sumOfScores=0;
            for(int i=0;i<3;i++)
            {
                Integer x3 = Integer.parseInt(scores[i]);
                sumOfScores += x3;
            }
            return (float)sumOfScores/maxValue;

        }
        catch (Exception e)
        {
            return -1f;
        }
    }
}