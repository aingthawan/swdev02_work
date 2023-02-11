package ex4;

import org.junit.Test;

public class week1_duplicateElementCheckTest {
    @Test
    public void test0() {
      int[] arr0 = {1, 2, 3, 4, 5, 5, 6, 7, 8, 9};                              // Test Input : Have Repeated Element
      boolean expected0 = true;
      boolean result = week1_duplicateElementsCheck.duplicateElementsCheck(arr0);
      assertArrayEquals(expected0, result);
    }

    @Test
    public void test1() {
      int[] arr1 = {1, 2, 3, 4, 5, 6, 7, 8, 9};                              // Test Input : No Repeated Element
      boolean expected1 = false;
      boolean result = week1_duplicateElementsCheck.duplicateElementsCheck(arr1);
      assertArrayEquals(expected1, result);
    }

    private void assertArrayEquals(boolean expected0, boolean result) {
    }
    
}
