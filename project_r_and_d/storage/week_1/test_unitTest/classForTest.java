package test_unitTest;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.Test;

public class classForTest {
    public static void main(int args) {
        //print args + 10
        System.out.println(args + 10);
        //return args;
    }


    @Test
    public void testClassForTest() {
        assertEquals(10, 10);
        assertEquals(20, 20);
        assertEquals(1, 1);
    }

}


