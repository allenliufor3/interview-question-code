package cn.javatiku.jdkproxy.demo;

import java.lang.reflect.Proxy;

public class HelloApplication {

	public static void main(String[] args) {
		// 从源码中得知，设置这个值，可以把生成的代理类，输出出来。
        System.getProperties().put("sun.misc.ProxyGenerator.saveGeneratedFiles", "true");
		IRunner helloRunner = new HelloRunner();
		HelloProxyInvocationHandler helloProxyInvocationHandler = new HelloProxyInvocationHandler(helloRunner);
		IRunner proxy = (IRunner) helloProxyInvocationHandler.getProxy();
		System.out.println("pm.getName:"+proxy.getClass().getName());
		proxy.doWork();
	}
}
