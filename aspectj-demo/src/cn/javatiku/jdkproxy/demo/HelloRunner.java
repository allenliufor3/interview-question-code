package cn.javatiku.jdkproxy.demo;

public class HelloRunner implements IRunner{
	
	@Override
	public boolean doWork() {
		System.out.println("it's running...");
		return true;
	}
}
