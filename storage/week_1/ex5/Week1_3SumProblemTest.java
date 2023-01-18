package ex5;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import org.junit.Test;

public class Week1_3SumProblemTest {
    @Test
    public void testSum0() {
      int[] arr0 = {0, -1, 2, -3, 1, -2};                              // Test Input 1 : Correct Answer
      int[][] expected0 = {{-3, 1, 2}, {-2, 0, 2}, {-1, 0, 1} };
      int[][] result = week1_3sumProblem.sum(arr0);
      assertArrayEquals(expected0, result);
    }

    @Test
    public void testSum1() {
      int[] arr1 = {-1, 0, 1, 2, -1, -4};
      int[][] expected1 = {{-1, -1, 2}, {-1, 0, 1}, {-1, 0, 1} };      // Test Input 2 : Correct Answer
      //int[][] expected1 = {{-1, -1, 2}, {-1, 0, 1}, {0, 0, 0} };     
      int[][] result = week1_3sumProblem.sum(arr1);
      assertArrayEquals(expected1, result);
    }

    @Test
    public void testSum2() {                                           // Test Empty Input : Return Null Correct Answer
      int[] arr2 = {1, 1, 1, 1, 1, 1};
      int[][] result = week1_3sumProblem.sum(arr2);
      assertArrayEquals(null, result);
    }
    
}