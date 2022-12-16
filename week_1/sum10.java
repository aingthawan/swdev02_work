package week_1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class sum10 {
    public static void main(String[] args) {
    // target file name
    String fileName = "input_sum10.txt";

    // This will reference one line at a time
    String line = null;

    try {
      // FileReader reads text files in the default encoding
      FileReader fileReader = new FileReader(fileName);

      // Wrap FileReader in BufferedReader
      BufferedReader bufferedReader = new BufferedReader(fileReader);

      // Read and print the file line by line
      while((line = bufferedReader.readLine()) != null) {
        System.out.println(line);
      }

      // Close the file and BufferedReader
      bufferedReader.close();
    }
    catch(IOException ex) {
      System.out.println("Error reading file '" + fileName + "'");
    }
  }
}

