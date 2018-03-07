import java.util.Random;

/**
 * @version V1.0 <br/>
 * @description: ${TODO}<br/>
 * @date 2018/3/7 13:40 <br/>
 */
public class Demo {

    public static int add(int a, int b) {
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return a + b;
    }

    public static void main(String[] args) {
        Random random = new Random();

        while (true) {
            System.err.println("result:" + add(random.nextInt(10), random.nextInt(10)));
        }
    }
}
