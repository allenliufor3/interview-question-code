import static com.sun.btrace.BTraceUtils.*;
import com.sun.btrace.annotations.*;

/**
 * A simple BTrace program that prints stack trace
 * whenever a class is loaded by a user-defined
 * class loader. We insert a return point probe in
 * ClassLoader.defineClass method to detect successful
 * class load.
 */
@BTrace public class Classload {
    @OnMethod(
            clazz="+java.lang.ClassLoader",
            method="defineClass",
            location=@Location(Kind.RETURN)
    )
    public static void defineclass(@Return Class cl) {
        println("loaded " +  Reflective.name(cl));
        Threads.jstack();
        println("==========================");
    }
}