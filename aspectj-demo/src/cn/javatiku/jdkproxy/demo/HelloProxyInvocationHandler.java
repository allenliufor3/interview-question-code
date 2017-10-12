package cn.javatiku.jdkproxy.demo;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class HelloProxyInvocationHandler implements InvocationHandler {

	private Object target;

	public HelloProxyInvocationHandler(Object target) {
		super();
		this.target = target;
	}

	private void beforeAdvice(Object proxy, Method method, Object[] args) {
		System.out.println(target.getClass().getName() + " : " + method.getName() + " before");
	}

	private void afterAdvice(Object proxy, Method method, Object[] args) {
		System.out.println(target.getClass().getName() + " : " + method.getName() + " after");
	}

	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
		beforeAdvice(proxy, method, args);
		Object result = method.invoke(target, args);
		afterAdvice(proxy, method, args);
		return result;
	}

	public Object getProxy() {
		return Proxy.newProxyInstance(Thread.currentThread().getContextClassLoader(), target.getClass().getInterfaces(), this);
	}

}
