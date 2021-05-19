public class Input {    
    public static void main(String[] args) {
        int a = 0;
        int a2 = 123;
        int a3 = -22;

        char b = 'b';
        char b2 = '1';
        char b3 = ' ';

        boolean c = true;
        boolean c2 = false;

        String d = "Hello world";
        String d2 = "My student id is 12345678";
        String d3 = "int char boolean true false 1";

        int i, j, k, abc, ab_123, func1, func_, __func_bar__;

        if (a > -1){
            a = a2;
        }
        else {
            a = a3;
            return 1;
        }
        if (a < 0){
            a = a + 1;
        }
        if (a == 1){
            a = a - 1;
        }
        if (a != 1){
            a = a * 0;
        }
        while (a <= 1){
            a = a / -1;
        }

        return;
    }
}
