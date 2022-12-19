package ex5;
import java.util.Arrays;

public class week1_3sumProblem {
  public static void main(String[] args) {
    int[] arr = {0, -1, 2, -3, 1, -2};

    // array sort
    //{-3, -2, -1, 0, 1, 2}
    Arrays.sort(arr);

    // loop through the array and find the 3 sum
    for (int i = 0; i < arr.length; i++) {
      int j = i + 1;
      int k = arr.length - 1;
      while (j < k) {
        int sum = arr[i] + arr[j] + arr[k];
        if (sum == 0) {
          // If sum = 0, then add three element to ans list
          System.out.println("(" + arr[i] + "," + arr[j] + "," + arr[k] + ")");
          break;
        } else if (sum < 0) {
          // if the 3 sum is negative, then move the left pointer  -- to the right to increase the sum
          j++;
        } else {
          // if the 3 sum is positive, then move the right pointer  -- to the left to decrease the sum
          k--;
        }
      }
    }
  }
}