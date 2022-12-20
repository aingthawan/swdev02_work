package ex4;
// Duplicated element check 
// O(n) is not over O(n2)

import java.util.HashSet;  
import java.util.Set;      // import for use Set<Integer>

/**
 * duplicateElementsCheck
 */
public class week1_duplicateElementsCheck {
    public static void main(String[] args) {
      int[] input_arr = {1, 2, 3, 4, 5, 5, 6, 7, 8, 9};
      System.out.println("");
      System.out.println("DUPLICATED ELEMENT CHECK");

      //call duplicateElementsCheck function
      if (duplicateElementsCheck(input_arr)){
        System.out.println("There are duplicated elements in the array");
      }else{
        System.out.println("There are no duplicated elements in the array");
      }
      System.out.println("");

    }

    public static boolean duplicateElementsCheck(int[] numbers){
      Set<Integer> set = new HashSet<Integer>();     // Create Array
      for (int i = 0; i < numbers.length; i++) {
        if (set.contains(numbers[i])) {              // If number already in array, then return true
          return true;
        }else{
          set.add(numbers[i]);                       // If number is unseen, keep in array
        }
      }
      return false;                                  // Loop end ,no duplicate element, return false
    }

  }



  ////// old code

  // System.out.println("DUPLICATED ELEMENT CHECK");
  
  //     // Track seen number (DICT)
  //     Set<Integer> seenNumbers = new HashSet<>();
  
  //     // Loop through the numbers array
  //     for (int num : numbers) { // "for each" loop
  //       // Found repeat display and end program
  //       if (seenNumbers.contains(num)) {
  //         System.out.println("Theres a repeated element in the array!");
  //         //exit program
  //         System.exit(0);
  //       } else {
  //         // add the number to the set
  //         seenNumbers.add(num);
  //       }
  //     }
  //     System.out.println("No repeated element in the array!");