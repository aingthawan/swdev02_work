// Duplicated element check 
// O(n) is not over O(n2)

import java.util.HashSet;  // import hashset
import java.util.Set;      // import for use Set<Integer>

/**
 * duplicateElementsCheck
 */
public class week1_duplicateElementsCheck {
    public static void main(String[] args) {
      int[] numbers = {1, 2, 3, 4, 5, 5, 6, 7, 8, 9};
      //int[] numbers = {1, 2, 3, 4};

      System.out.println("DUPLICATED ELEMENT CHECK");
  
      // Track seen number
      Set<Integer> seenNumbers = new HashSet<>();
  
      // Loop through the numbers array
      for (int num : numbers) {
        // If we have seen the number before, print it
        if (seenNumbers.contains(num)) {
          System.out.println("Theres a repeated element in the array!");
          System.exit(0);
        } else {
          // Otherwise, add the number to the set
          seenNumbers.add(num);
        }
      }
      System.out.println("No repeated element in the array!");
    }
  }