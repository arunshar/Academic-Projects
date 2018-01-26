/**
 * Members class for handling members instance
 * @author Jayashree Chandrasekaran
 * @author Sujit Singh
 * @author Harsh Nayak
 * @author Arun Sharma
 * @author Fengyu Wu
 */
public class Members {

    /**
     * Checks whether the member count is between 2-7
     * @param members the number of members
     * @return boolean value
     */
    public boolean checkMembers(int members)
    {
        if(members>7 || members<2)
        {
            return false;
        }
        return true;

    }

    /**
     *
     * @return returns the dummy names of all possible members
     */
    public String[] getNames()
    {
        String[] names = {"1","2","3","4","5","6","7"};
        return names;
    }

    /**
     * checks if the user has put null or invalid input in the input member stage
     * @param input number of members input by the user
     * @return boolean value
     */
    public boolean checkUserInput(String input)
    {

        try
        {
            int convertToInt = Integer.parseInt(input);
            return true;
        }
        catch (Exception e)
        {
            return false;
        }
    }


}
