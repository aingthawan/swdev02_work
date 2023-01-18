package ex5;

import java.util.ArrayList;
import java.util.Arrays;

public class week1_3sumProblem {
  public static int[][] sum(int[] arr){
    // Create an empty list to store the 3 sum answers
    ArrayList<int[]> ans = new ArrayList<>();

    // Sort the array
    Arrays.sort(arr);

    // Loop through the array and find the 3 sum
    for (int i = 0; i < arr.length; i++) {
      int j = i + 1;
      int k = arr.length - 1;
      while (j < k) {
        int sum = arr[i] + arr[j] + arr[k];
        if (sum == 0) {
          // If sum = 0, then add three element to ans list
          ans.add(new int[]{arr[i], arr[j], arr[k]});
          j++;
          k--;
        } else if (sum < 0) {
          // if the 3 sum is negative, then move the left pointer to the right to increase the sum
          j++;
        } else {
          // if the 3 sum is positive, then move the right pointer to the left to decrease the sum
          k--;
        }
      }
    }

    // Convert the list to an array and return the answer
    //return ans.toArray(new int[ans.size()][]);

    if (ans.toArray(new int[ans.size()][]).length == 0){
      return null;
    }else{
      return ans.toArray(new int[ans.size()][]);
    }

  }

  public static void main(String[] args) {
    // int[] arr = {10, 10, 10, 10, 10, 10};
    // int[] arr = {-1, 0, 1, 2, -1, -4};
	  int[] arr = {0, -1, 2, -3, 1, -2};
    int[][] ans = sum(arr);
    
    if (ans == null){
      System.out.println("No 3 sum");
    }else{
      for (int[] a : ans) {
        System.out.print(Arrays.toString(a) + " ");
      }
    }
    
  }
  
}

